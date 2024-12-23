from dagger import Container, dag, function, object_type, Secret, File, Directory, DefaultPath, CacheVolume, JSON

from typing import Self, Annotated, Tuple


from datetime import datetime
import time
import json


@object_type
class Shadeform:

    name: str
    shade_token: Secret
    vm_id: str | None
    ssh_key: File | None
    cache: CacheVolume
    template_file: File


    @classmethod
    async def create(
        cls,
        name: str,
        shade_token: Secret,
        vm_id: str | None,
        ssh_key: File | None,
        cache: CacheVolume | None,
        template_file: Annotated[File, DefaultPath("./vm-template.json")]
    ):
        """ 
        Initialize module with cache associated to the VM name
        """
        if cache is None:
            cache = dag.cache_volume(name)
        return cls(name=name,ssh_key=ssh_key,cache=cache,shade_token=shade_token,vm_id=vm_id, template_file=template_file)

    @function
    def client(self) -> Container:
        """
        Return a CURL debug client with cache (vm information) mounted.
        """
        return (
            dag.container()
            .from_("alpine:latest")
            .with_exec(["apk", "add", "jq", "curl"])
            .with_env_variable("CACHE", str(datetime.now()))
            .with_mounted_cache(path="/cache", cache=self.cache)
        )

    @function
    async def exists(self):

        return await (
                    self.client()
                    .with_exec(["jq", "-r",".id", "/cache/vm_id.json"])
                    )

    @function
    async def create_vm(
            self, 
            cloud: str,
            region: str,
            shade_instance_type: str,
            shade_cloud: str,
        ) -> Container:
        """
        Returns a container executing all the needed steps for creating a machine starting from passed parameters
        """

        token = await self.shade_token.plaintext()

        config_file = {
            "cloud": cloud,
            "region": region,
            "shade_instance_type": shade_instance_type,
            "shade_cloud": shade_cloud,
            "name": self.name
        }


        try:
            await self.exists()
        except: 
            try:
                return await (
                        self.client()
                         .with_file(
                            path="/opt/data.json",
                            source=dag.dagger_templates().compile_template(json_values=JSON(json.dumps(config_file)), template_file=self.template_file)
                         )
                         .with_exec(["cp", "/opt/data.json", "/cache/data.json"])
                         .with_exec(["cat", "/cache/data.json"])
                         .with_exec([
                                "curl", "--fail-with-body",
                                "--request", "POST",
                                "--url", "https://api.shadeform.ai/v1/instances/create",
                                "--header", "Content-Type: application/json",
                                "--header", f"X-API-KEY: {token}",
                                "--data", "@/cache/data.json",
                                "-o", "/cache/vm_id.json"
                            ])
                        .with_exec(["jq", "-r",".id", "/cache/vm_id.json"])
                        )
            except Exception as ex:
                try: 
                    raise Exception(await self.client().with_exec(["cat", "/cache/vm_id.json"]).stdout())
                except:
                    raise ex
        return dag.container()

    @function
    async def get_vm_id(self) -> str:
        """
        Return the VM ID
        """

        return await (
            self.client()
            .with_exec(["jq", "-r",".id", "/cache/vm_id.json"]).stdout()
        )

    @function
    async def get_vm_info(
        self
        ) -> str:
        """
        Return the VM info JSON 
        """

        token = await self.shade_token.plaintext()
        id = await self.get_vm_id()

        try:
            return await (
             self.client()
             .with_exec([
                    "curl", "--fail-with-body",
                    "--request", "GET",
                    "--url", f"https://api.shadeform.ai/v1/instances/{id.strip('\n')}/info",
                    "--header", f"X-API-KEY: {token}",
                    "-o", "/cache/vm_info.json"
                ]).stdout()
            )
        except:
            raise Exception(await self.client().with_exec(["cat", "/cache/vm_info.json"]).stdout())

    @function
    async def get_available_list(
        self,
        gpu_type: str,
        n_gpus: int
        ) -> str:
        """
        Return a list of available instances with the indicated boards sorted by price 
        """

        token = await self.shade_token.plaintext()

        try:
            return await (
             self.client()
             .with_exec([
                    "curl", "--fail-with-body",
                    "--request", "GET",
                    "--url", f"https://api.shadeform.ai/v1/instances/types?gpu_type={gpu_type}&num_gpus={n_gpus}&available=true&sort=price",
                    "--header", f"X-API-KEY: {token}",
                    "-o", "/cache/vm_list.json"
                ])
            .with_exec(["jq", "-r",".instance_types[0]", "/cache/vm_list.json"]).stdout()
            )
        except:
            raise Exception(await self.client().with_exec(["cat", "/cache/vm_info.json"]).stdout())

    @function
    async def get_vm_status(self) -> str:
        """
        Print the VM status 
        """

        await self.get_vm_info()

        return await (
            self.client()
            .with_exec(["cat", "/cache/vm_info.json"])
            .with_exec(["jq", "-r",".status", "/cache/vm_info.json"]).stdout()
        )

    @function
    async def get_vm_ip(self) -> str:
        """
        Print the VM IP 
        """

        await self.get_vm_info()

        return await (
            self.client()
            .with_exec(["cat", "/cache/vm_info.json"])
            .with_exec(["jq", "-r",".ip", "/cache/vm_info.json"]).stdout()
        )

    @function
    async def get_vm_user(self) -> str:
        """
        Print the VM user to use for SSH connection
        """

        await self.get_vm_info()

        return await (
            self.client()
            .with_exec(["cat", "/cache/vm_info.json"])
            .with_exec(["jq", "-r",".ssh_user", "/cache/vm_info.json"]).stdout()
        )

    @function
    async def vm_ready(self, max_retries: int = 10) -> str:
        """
        Wait for VM to be ready and return its ID
        """

        status = ""
        retries = 0
        while status != "active":
            if retries > 0:
                time.sleep(60)
            status = await self.get_vm_status()
            status = status.strip('\n')
            print(status)
            retries += 1
            if retries > max_retries:
                await self.delete_vm()
                raise Exception("Timeout waiting for node to come up")

        return await (
            self.client()
            .with_exec(["jq", "-r",".id", "/cache/vm_id.json"]).stdout()
        )

    @function
    async def create_n_check(
            self,
            cloud: str = "hyperstack",
            region: str = "canada-1",
            shade_instance_type: str = "A6000",
            shade_cloud: str = "true",
        ) -> str:
        """
        Create a VM and wait for its creation to succeed
        """
        await self.create_vm(cloud, region, shade_instance_type, shade_cloud) 
        
        return await self.vm_ready()


    @function
    async def delete_vm(
        self
        ) -> str:
        """
        Delete VM
        """

        token = await self.shade_token.plaintext()
        id = await self.get_vm_id()


        return await (
         self.client()
            .with_exec([
                "curl", "--fail-with-body",
                "--request", "POST",
                "--url", f"https://api.shadeform.ai/v1/instances/{id.strip('\n')}/delete",
                "--header", f"X-API-KEY: {token}"
            ])
            .with_exec(["sh", "-c", "rm /cache/vm_id.json"])
            .stdout()
        )


    @function
    async def exec_ssh_command(
        self,
        command: str,
        ssh_key: File,
        ) -> str:
        """
        execute the provided through automatic ssh command 
        """
        host = await self.get_vm_ip()
        ssh_user = await self.get_vm_user()
    
        return await (
            dag.container()
                .from_("ubuntu")
                .with_exec(["bash", "-c", "apt update && apt install -y openssh-client"])
                .with_mounted_file(path="/opt/key.key",source=ssh_key)
                .with_exec([
                    "ssh",
                    "-i", "/opt/key.key",
                    "-o", "StrictHostKeyChecking=no",
                    f"{ssh_user.strip('\n')}@{host.strip('\n')}",
                    f"{command}"
                ]).stdout()
        )

    @function
    async def copy_file(
        self,
        ssh_key: File,
        file: File,
        destination: str,
        ) -> str:
        """
        Copy a local file to the remote VM
        """
        host = await self.get_vm_ip()
        ssh_user = await self.get_vm_user()
    
        return await (
            dag.container()
                .from_("ubuntu")
                .with_exec(["bash", "-c", "apt update && apt install -y openssh-client"])
                .with_mounted_file(path="/opt/key.key",source=ssh_key)
                .with_mounted_file(path="/opt/file",source=file)
                .with_exec([
                    "scp",
                    "-i", "/opt/key.key",
                    "-o", "StrictHostKeyChecking=no",
                    "/opt/file", f"{ssh_user.strip('\n')}@{host.strip('\n')}:{destination}"
                ]).stdout()
        )

    @function
    async def copy_dir(
        self,
        ssh_key: File,
        dir: Directory,
        destination: str,
        ) -> str:
        """
        Copy a local directory to the remote VM
        """
        host = await self.get_vm_ip()
        ssh_user = await self.get_vm_user()
    
        return await (
            dag.container()
                .from_("ubuntu")
                .with_exec(["bash", "-c", "apt update && apt install -y openssh-client"])
                .with_mounted_file(path="/opt/key.key",source=ssh_key)
                .with_mounted_directory(path="/opt/dir",source=dir)
                .with_exec([
                    "scp",
                    "-r",
                    "-i", "/opt/key.key",
                    "-o", "StrictHostKeyChecking=no",
                    "/opt/dir", f"{ssh_user.strip('\n')}@{host.strip('\n')}:{destination}"
                ]).stdout()
        )

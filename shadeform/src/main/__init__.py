"""A generated module for Shadeform functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

from dagger import Container, dag, function, object_type, Secret, File, Directory, DefaultPath, CacheVolume
from typing import Self, Annotated, Tuple


from datetime import datetime
import time


# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


@object_type
class Shadeform:
    name: str
    shade_token: Secret
    vm_id: str | None
    ssh_key: File | None
    cache: CacheVolume

    @classmethod
    async def create(
        cls,
        name: str,
    shade_token: Secret,
    vm_id: str | None,
    ssh_key: File | None,
        cache: CacheVolume | None
    ):
        if cache is None:
            cache = dag.cache_volume(name)
        return cls(name=name,ssh_key=ssh_key,cache=cache,shade_token=shade_token,vm_id=vm_id)

    @function
    def client(self) -> Container:
        return (
            dag.container()
            .from_("alpine:latest")
            .with_exec(["apk", "add", "jq", "curl"])
            .with_env_variable("CACHE", str(datetime.now()))
            .with_mounted_cache(path="/cache", cache=self.cache)
        )

    # TODO: what happens if multiple create are done?
    @function
    async def create_vm(
            self, 
            config: Annotated[File, DefaultPath("./data.json")] 
        ) -> bool:
        """Returns a container that echoes whatever string argument is provided"""
        token = await self.shade_token.plaintext()

        await (
            self.client()
             .with_mounted_file(path="/opt/data.json", source=config)
             .with_exec([
                    "curl",
                    "--request", "POST",
                    "--url", "https://api.shadeform.ai/v1/instances/create",
                    "--header", "Content-Type: application/json",
                    "--header", f"X-API-KEY: {token}",
                    "--data", "@/opt/data.json",
                    "-o", "/cache/vm_id.json"
                ])
            )

        await self.vm_ready()
        return True

    @function
    async def get_vm_id(self) -> str:
        """Returns lines that match a pattern in the files of the provided Directory"""

        return await (
            self.client()
            .with_exec(["jq", "-r",".id", "/cache/vm_id.json"]).stdout()
        )

    @function
    async def get_vm_info(
        self
        ) -> str:
        token = await self.shade_token.plaintext()
        id = await self.get_vm_id()

        return await (
         self.client()
         .with_exec([
                "curl",
                "--request", "GET",
                "--url", f"https://api.shadeform.ai/v1/instances/{id.strip('\n')}/info",
                "--header", f"X-API-KEY: {token}",
                "-o", "/cache/vm_info.json"
            ]).stdout()
        )

    @function
    async def get_vm_status(self) -> str:

        await self.get_vm_info()

        return await (
            self.client()
            .with_exec(["jq", "-r",".status", "/cache/vm_info.json"]).stdout()
        )

    @function
    async def vm_ready(self, max_retries: int = 10) -> bool:

        status = ""
        retries = 0
        while status != "active":
            time.sleep(60)
            status = await self.get_vm_status()
            status = status.strip('\n')
            print(status)
            retries += 1
            if retries > max_retries:
                await self.delete_vm()
                raise Exception("Timeout waiting for node to come up")

        return True

    @function
    async def delete_vm(
        self
        ) -> str:
        token = await self.shade_token.plaintext()
        id = await self.get_vm_id()

        return await (
         self.client()
         .with_exec([
                "curl",
                "--request", "DELETE",
                "--url", f"https://api.shadeform.ai/v1/instances/{id.strip('\n')}",
                "--header", f"X-API-KEY: {token}"
            ]).stdout()
        )

    @function
    async def get_ssh_key(
        self
        ) -> Self:

        token = await self.shade_token.plaintext()
        self.ssh_key = await (
            dag.container()
             .from_("quay.io/curl/curl")
             .with_mounted_cache(path="/opt/cache", cache=self.cache)
             .with_exec([
                    "--request", "GET",
                    "--url", f"https://api.shadeform.ai/v1/instances/{self.vm_id}/info",
                    "--header", f"X-API-KEY: {token}",
                    "-o", "/opt/cache/vm_info.json"
                ], use_entrypoint=True)
                .file(path="/opt/key.key")
        )

        return self

    @function
    async def exec_ssh_command(
        self,
        command: str,
        ) -> str:
        """ """
    
        if not self.ssh_key:
            await self.get_ssh_key()

        if not self.ssh_key:
            raise Exception("No ssh key found")

        return await (
            dag.container()
                .from_("ubuntu")
                .with_mounted_file(path="/opt/key.key",source=self.ssh_key)
                .with_exec([
            "ssh",
            "-i", "/opt/key.key",
            "-q", f"\"{command}\""
                    ]).stdout()
        )



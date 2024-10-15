import dagger
from dagger import dag, function, object_type
from collections.abc import Coroutine


@object_type
class Python:
    @function
    async def shadeform(
            self,
            name: str,
            shade_token: dagger.Secret,
            ssh_key: dagger.File,
            install_script: dagger.File,
            interlink_key: dagger.File,
            interlink_endpoint: str,
            interlink_port: int
        ) -> str:
        """
        Demo creating a VM and install software and launching deamons on that
        """

        cloud = "imwt"
        region = "us-central-2"
        shade_instance_type = "A6000"
        shade_cloud = "true"
        
        await (
            dag.shadeform(name, shade_token)
            .create_n_check(
                cloud=cloud,
                region=region,
                shade_instance_type=shade_instance_type,
                shade_cloud=shade_cloud)
        )

        await dag.shadeform(name, shade_token).copy_file(ssh_key=ssh_key, file=install_script, destination="/opt/install.sh")
        await dag.shadeform(name, shade_token).copy_file(ssh_key=ssh_key, file=interlink_key, destination="/opt/ssh.key")

        return await dag.shadeform(name, shade_token).exec_ssh_command(ssh_key=ssh_key, command=f"bash -c \"/opt/install.sh /opt/ssh.key {interlink_endpoint} {interlink_port}\"")

    @function
    async def shadeform__create_n_check(
            self,
            name: str,
            shade_token: dagger.Secret,
            cloud: str,
            region: str,
            shade_instance_type: str,
            shade_cloud: str,
        ) -> str:
        """
        This is an example of creating a VM and checking when done
        """

        return await (
            dag.shadeform(name, shade_token)
            .create_n_check(
                cloud=cloud,
                region=region,
                shade_instance_type=shade_instance_type,
                shade_cloud=shade_cloud)
        )



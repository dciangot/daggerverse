import dagger
import time
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
        Demo creating a VM and install software (e.g. interlink) and launching deamons
        """

        cloud = "hyperstack"
        region = "canada-1"
        shade_instance_type = "A6000"
        shade_cloud = "true"
        
        # Create a VM and wait for it to be ready
        await (
            dag.shadeform(name, shade_token)
            .create_n_check(
                cloud=cloud,
                region=region,
                shade_instance_type=shade_instance_type,
                shade_cloud=shade_cloud)
        )

        #time.sleep(120)

        # Copy the local install script on the VM
        print (
            await (
                dag.shadeform(name, shade_token)
                .copy_file(
                    ssh_key=ssh_key,
                    file=install_script,
                    destination="/tmp/install.sh"
                )
            )
        )

        # Copy additional files
        print( 
            await (
                dag.shadeform(name, shade_token)
                .copy_file(
                    ssh_key=ssh_key,
                    file=interlink_key,
                    destination="/tmp/ssh.key"
                )
            )
        )

        # Execute the installation script
        return await (
            dag.shadeform(name, shade_token)
            .exec_ssh_command(
                ssh_key=ssh_key,
                command=f"bash -c \"/tmp/install.sh start /tmp/ssh.key {interlink_endpoint} {interlink_port}\""
            )
        )

    @function
    async def shadeform__delete_vm(
            self,
            name: str,
            shade_token: dagger.Secret,
        ) -> str:
        """
        This is an example of deleting a VM
        """
        return await (
            dag.shadeform(name, shade_token)
            .delete_vm()
        )

    @function
    async def shadeform__create_n_check(
            self,
            name: str,
            shade_token: dagger.Secret,
        ) -> str:
        """
        This is an example of creating a VM and checking when done
        """

        cloud = "imwt"
        region = "us-central-2"
        shade_instance_type = "A6000"
        shade_cloud = "true"

        return await (
            dag.shadeform(name, shade_token)
            .create_n_check(
                cloud=cloud,
                region=region,
                shade_instance_type=shade_instance_type,
                shade_cloud=shade_cloud)
        )



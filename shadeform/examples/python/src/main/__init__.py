import dagger
from dagger import dag, function, object_type
from collections.abc import Coroutine

# NOTE: it's recommended to move your code into other files in this package
# and keep __init__.py for imports only, according to Python's convention.
# The only requirement is that Dagger needs to be able to import a package
# called "main", so as long as the files are imported here, they should be
# available to Dagger.


@object_type
class Python:
    @function
    async def shadeform_create_n_check(
            self,
            name: str,
            shade_token: dagger.Secret,
            cloud: str,
            region: str,
            shade_instance_type: str,
            shade_cloud: str,
            # interlink_key: File,
            # interlink_endpoint: str,
            # interlink_port: int
        ) -> str:

        return await (
            dag.shadeform(name, shade_token)
            .create_n_check(
                cloud=cloud,
                region=region,
                shade_instance_type=shade_instance_type,
                shade_cloud=shade_cloud)
        )



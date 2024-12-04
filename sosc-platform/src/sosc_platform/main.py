import dagger
from dagger import dag, function, object_type


@object_type
class SoscPlatform:
    name: str
    context_dir: dagger.Directory
    cache: dagger.CacheVolume

    @classmethod
    async def create(cls, name: str, context_dir: dagger.Directory):
        return cls(name=name, context_dir=context_dir, cache=dag.cache_volume("name"))

    @function
    def build_image(self) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return (
            dag.container()
            .with_directory("/src", self.context_dir)
            .with_workdir("/src")
            .directory("/src")
            .docker_build()
        )

    @function
    def papermill(
        self, notebook: dagger.File, param_file: dagger.File
    ) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return (
            self.build_image()
            .with_mounted_file("/home/jovyan/notebook.ipynb", source=notebook)
            .with_mounted_file("/home/jovyan/params.json", source=param_file)
            .with_mounted_cache("/home/jovyan/outputs", self.cache)
        )

    @function
    async def sosc(self, jupyter_secret: dagger.Secret) -> dagger.Service:
        """Returns a container that echoes whatever string argument is provided"""
        token = await jupyter_secret.plaintext()

        return (
            self.build_image()
            .with_exec(
                [
                    "minio",
                    "server",
                    "/home/jovyan/persistent_data/minio",
                    "--console-address",
                    ":9001",
                ]
            )
            .with_mounted_cache("/home/jovyan/persistent_data", self.cache)
            .with_exec(["jupyter", "lab", f"--IdentityProvider.token={token}"])
            .with_exposed_port(8888)
            .as_service()
        )

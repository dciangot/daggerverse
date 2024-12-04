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
            .with_mounted_cache("/home/jovyan/persistent_data", self.cache)
            .with_user("root")
            .with_exec(["chown", "-R", "jovyan", "/home/jovyan/persistent_data"])
            .with_user("jovyan")
            .with_env_variable(name="MINIO_ROOT_USER", value="minio")
            .with_env_variable(name="MINIO_ROOT_PASSWORD", value="sosc2024")
            .with_env_variable(
                name="MINIO_BROWSER_REDIRECT_URL",
                value="http://localhost:8888/object-storage/",
            )
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
        )

    @function
    async def sosc(self, jupyter_secret: dagger.Secret) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        token = await jupyter_secret.plaintext()

        return (
            self.build_image()
            .with_workdir("/home/jovyan")
            .with_exec(
                ["jupyter", "lab", f"--IdentityProvider.token={token}", "--ip=0.0.0.0"]
            )
            .with_exposed_port(8888)
            # .as_service()
        )

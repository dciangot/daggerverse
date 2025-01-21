from dagger import dag, function, object_type
from dagger.client.gen import Container, File


@object_type
class Interlink:
    @function
    async def interlink_cluster(self, values: File) -> Container:
        k3s = dag.k3_s("test")
        server = k3s.server()

        await server.start()

        return (
            dag.container()
            .from_("alpine/helm")
            .with_mounted_file("/.kube/config", k3s.config())
            .with_mounted_file("/values.yaml", values)
            .with_env_variable("KUBECONFIG", "/.kube/config")
            .with_exec(
                [
                    "helm",
                    "install",
                    "--wait",
                    "--debug",
                    "my-node",
                    "oci://ghcr.io/intertwin-eu/interlink-helm-chart/interlink",
                    "--values",
                    "/values.yaml",
                ]
            )
        )

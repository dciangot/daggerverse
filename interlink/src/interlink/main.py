from dagger import dag, function, object_type
from dagger.client.gen import Container, File, Service


@object_type
class Interlink:
    name: str

    @function
    async def cluster_config(self, local: bool = False) -> File:
        k3s = dag.k3_s(self.name)

        return k3s.config(local=local)

    @function
    async def interlink_cluster(self, values: File, vk_name: str) -> Service:
        k3s = dag.k3_s(self.name)
        server = k3s.server()

        svc = await server.start()

        await (
            dag.container()
            .from_("alpine/helm")
            .with_exec(["apk", "add", "kubectl"])
            .with_mounted_file("/.kube/config", k3s.config())
            .with_mounted_file("/values.yaml", values)
            .with_env_variable("KUBECONFIG", "/.kube/config")
            .with_exec(
                [
                    "helm",
                    "install",
                    "--debug",
                    "my-node",
                    "oci://ghcr.io/intertwin-eu/interlink-helm-chart/interlink",
                    "--values",
                    "/values.yaml",
                ]
            )
            .with_exec(
                [
                    "kubectl",
                    "wait",
                    "--for=condition=Ready",
                    f"node/{vk_name}",
                    "--timeout=300s",
                ]
            ).stdout()
            
        )

        return svc

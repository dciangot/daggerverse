from typing import Annotated

from dagger import Doc, dag, function, object_type
from dagger.client.gen import File, Secret, Service


@object_type
class Interlink:
    name: str

    @function
    async def cluster_config(
        self,
        local: Annotated[bool, Doc("Whether to access the cluster from localhost.")] = False,
    ) -> File:
        """Returns the config file for the k3s cluster."""
        k3s = dag.k3_s(self.name)

        return k3s.config(local=local)

    @function
    async def interlink_cluster(
        self,
        values: Annotated[Secret, Doc("Configuration file for interLink installer.")],
        wait: Annotated[
            int,
            Doc(
                "Sleep time (seconds) needed to wait for the VK to appear in the k3s cluster."
            ),
        ] = 60,
    ) -> Service:
        """Get interLink VK deployed on a k3s cluster. Returns k3s as a service."""
        k3s = dag.k3_s(self.name)
        server = k3s.server()

        svc = await server.start()

        interlink_container = (
            k3s.container()
            .from_("alpine/helm")
            .with_exec(["apk", "add", "kubectl"])
            .with_mounted_file("/.kube/config", k3s.config())
            .with_mounted_secret("/values.yaml", values)
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
        )

        # Force the interlink container to be created
        await interlink_container.stdout()
        import time

        # Wait for the VK to be spawned
        time.sleep(wait)

        # Wait for the VK to be ready
        await (
            interlink_container
            # .terminal()
            .with_exec(
                [
                    "kubectl",
                    "wait",
                    "--for=condition=Ready",
                    "nodes",
                    "--all",
                    "--timeout=300s",
                ]
            ).stdout()
        )

        return svc

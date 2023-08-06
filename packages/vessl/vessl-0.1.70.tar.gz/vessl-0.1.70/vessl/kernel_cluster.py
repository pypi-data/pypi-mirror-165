import subprocess
from time import sleep
from typing import List, Optional

from kubernetes import config, client
from kubernetes.client import V1Secret
from openapi_client.models import (
    ClusterUpdateAPIInput,
    ResponseKernelClusterInfo,
    ResponseKernelClusterNodeInfo,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.util.exception import ClusterAlreadyExistsError, ClusterNotFoundError, InvalidKernelClusterError, VesslApiException
from vessl.util import logger

def create_cluster(
    cluster_name: str,
    kubernetes_namespace: str = "vessl",
    extra_helm_values: List[str] = [], **kwargs) -> ResponseKernelClusterInfo:
    """Create a VESSL cluster by installing VESSL agent to given Kubernetes namespace.
    `**kwargs`.

    Args:
        cluster_name(str): Cluster name.
        kubernetes_namespace(str): Kubernetes namespace to install VESSL agent. defaults to "vessl".
        extra_helm_values(list[str]): Helm values to pass to cluster install command. See https://github.com/vessl-ai/cluster-resources/blob/main/helm-chart/values.yaml for available Helm values.

    Example:
        ```python
        vessl.install_cluster(
            cluster_name="seoul-cluster",
        )
        ```
    """

    _check_existing_vessl_installation()

    agent_access_token = vessl_api.custom_cluster_key_api(
        organization_name=_get_organization_name(**kwargs),
    ).access_token

    logger.debug(f"cluster name: '{cluster_name}'")
    logger.debug(f"access token: '{agent_access_token}'")

    subprocess.check_call(["helm", "repo", "add", "vessl", "https://vessl-ai.github.io/cluster-resources/helm-chart"])
    subprocess.check_call(["helm", "repo", "update"])

    cluster_install_command = [
        "helm", "install", "vessl", "vessl/cluster-resources",
        "--namespace", kubernetes_namespace,
        "--create-namespace",
        "--set", f"agent.clusterName={cluster_name}",
        "--set", f"agent.accessToken={agent_access_token}",
    ]

    for helm_value in extra_helm_values:
        cluster_install_command.extend(["--set", helm_value])
    subprocess.check_call(cluster_install_command)

    logger.warn("VESSL cluster agent installed. Waiting for the agent to be connected with VESSL...")
    for attempts in range(18):
        sleep(10)
        try:
            return vessl_api.cluster_read_api(
                organization_name=_get_organization_name(**kwargs),
                cluster_id=cluster_name,
            )
        except VesslApiException as e:
            if e.code == "NotFound":
                continue
            raise e

    raise ClusterNotFoundError("Timeout for checking agent connection; Please check agent log for more information.")

def _check_existing_vessl_installation():
    """Check if there is existing vessl installation in current Kubernetes cluster."""
    # Load kubenetes config

    try:
        config.load_kube_config(config_file="/var/lib/k0s/pki/admin.conf")
    except config.config_exception.ConfigException:
        # Try with default KUBECONFIG location if k0s conf is not found
        config.load_kube_config()
    _, active_context = config.list_kube_config_contexts()
    if not active_context:
        raise ClusterNotFoundError("Kubernetes cluster not found in local context. Do you have active Kubernetes cluster up & running?")

    # Find secret with label=app.kubernetes.io/managed-by=Helm, annotation=meta.helm.sh/release-name=vessl
    v1 = client.CoreV1Api()
    secrets = v1.list_secret_for_all_namespaces(label_selector="app.kubernetes.io/managed-by=Helm")
    vessl_secret: Optional[V1Secret] = None
    for secret in secrets.items:
        if secret.metadata and secret.metadata.annotations and secret.metadata.annotations.get("meta.helm.sh/release-name") == "vessl":
            vessl_secret = secret
    if vessl_secret is not None:
        # VESSL agent token is found - there is existing cluster in current kubernetes cluster
        raise ClusterAlreadyExistsError("VESSL agent already existing in Current kubernetes cluster.")


def read_cluster(cluster_name: str, **kwargs) -> ResponseKernelClusterInfo:
    """Read cluster in the default organization. If you want to override the
    default organization, then pass `organization_name` as `**kwargs`.

    Args:
        cluster_name(str): Cluster name.

    Example:
        ```python
        vessl.read_cluster(
            cluster_name="seoul-cluster",
        )
        ```
    """
    kernel_clusters = list_clusters(**kwargs)
    kernel_clusters = {x.name: x for x in kernel_clusters}

    if cluster_name not in kernel_clusters:
        raise InvalidKernelClusterError(f"Kernel cluster not found: {cluster_name}")
    return kernel_clusters[cluster_name]


def list_clusters(**kwargs) -> List[ResponseKernelClusterInfo]:
    """List clusters in the default organization. If you want to override the
    default organization, then pass `organization_name` as `**kwargs`.

    Example:
        ```python
        vessl.list_clusters()
        ```
    """
    return vessl_api.cluster_list_api(
        organization_name=_get_organization_name(**kwargs),
    ).clusters


def delete_cluster(cluster_id: int, **kwargs) -> object:
    """Delete custom cluster in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.

    Example:
        ```python
        vessl.delete_cluster(
            cluster_id=1,
        )
        ```
    """
    return vessl_api.cluster_delete_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    )


def rename_cluster(
    cluster_id: int, new_cluster_name: str, **kwargs
) -> ResponseKernelClusterInfo:
    """Rename custom cluster in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.
        new_cluster_name(str): Cluster name to change.

    Example:
        ```python
        vessl.rename_cluster(
            cluster_id=1,
            new_cluster_name="seoul-cluster-2",
        )
        ```
    """
    return vessl_api.cluster_update_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
        custom_cluster_update_api_input=ClusterUpdateAPIInput(
            name=new_cluster_name,
        ),
    )


def list_cluster_nodes(
    cluster_id: int, **kwargs
) -> List[ResponseKernelClusterNodeInfo]:
    """List custom cluster nodes in the default organization. If you want to
    override the default organization, then pass `organization_name` as
    `**kwargs`.

    Args:
        cluster_id(int): Cluster ID.

    Example:
        ```python
        vessl.list_cluster_nodes(
            cluster_id=1,
        )
        ```
    """
    return vessl_api.custom_cluster_node_list_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    ).nodes

import os
import time
import base64
from typing import Any, Dict, Optional, Union
from table_logger import table_logger

from kubernetes import client as k8s_client
from kubernetes import config as k8s_config
from kubernetes import watch as k8s_watch
from kubernetes.client.models import (
    V1Namespace,
    V1ServiceAccount,
    V1Secret,
    V1Container,
    V1Pod,
    V1PodStatus,
    V1PodCondition,
    V1ContainerState,
    V1ResourceRequirements,
    V1ObjectMeta,
    V1ObjectReference,
    V1LocalObjectReference,
    V1LimitRangeSpec,
    V1LimitRange,
    V1LimitRangeItem,
    V1LimitRangeList
)


from kubernetes.client.rest import ApiException
from kubernetes.config.config_exception import ConfigException

from .schema import ResourceSpec, Spec
from .enums import (
    PodStatus,
    PodConditionType,
    PodConditionStatus,
)


__all__ = [
    "KubernetesManager",
]


def _is_running_in_k8s():
    return os.path.isdir('/var/run/secrets/kubernetes.io/')


class KubernetesManager:

    # Reserved: for multi-cluster
    # See: https://github.com/kubernetes-client/python/blob/master/examples/multiple_clusters.py
    # contexts, active_context = config.list_kube_config_contexts()

    client: k8s_client.CoreV1Api
    crd_client: k8s_client.CustomObjectsApi

    @staticmethod
    def set_default_config(
            apiserver_host,
            verify_ssl: bool=True,
            token: str=None,
            username: str=None,
            password: str = None) -> k8s_client.Configuration:
        
        api_key: Union[Dict, Any]
        if token:
            api_key = {"authorization": "Bearer " + token}
        else:
            api_key = None
        config = k8s_client.Configuration(
            host=apiserver_host,
            api_key=api_key)
        config.verify_ssl = verify_ssl

        return config
    
    
    def watch_pod(
            self,
            name: str,
            namespace: str = "default",
            label_selector: Dict[str, str] = None,
            timeout_seconds: int = 600
            ):
        
        log_table = table_logger.TableLogger(
            columns='NAME,READY',
            colwidth={'NAME': 20, 'READY': 10},
            border=False,
        )

        stream = k8s_watch.Watch().stream(
            self.client.list_namespaced_pod,
            namespace=namespace,
            label_selector=label_selector,
            resource_version=None,
            timeout_seconds=timeout_seconds,
        )
        for event in stream:
            # pod = event.object
            # pod_name = pod.metadata.name
            pod = event['object']
            pod_name = pod['metadata']['name']
            if name != pod_name:
                continue
            else:
                if pod.get('status', ''):
                    status = PodStatus.UNKNOWN
                    for condition in pod['status'].get('conditions', {}):
                        if condition.get('type', '') ==  PodConditionType.READY:
                            status = condition.get('status', PodConditionStatus.UNKNOWN)
                    log_table(pod_name, status)
                else:
                    log_table(pod_name, PodStatus.UNKNOWN)
                    time.sleep(2)
                    continue

    def __init__(
            self,
            config_dict:dict = None,
            configuration: Optional[k8s_client.Configuration] = None,
            config_file=None,
            context=None,
            persist_config=True,
            ) -> None:
        
        try:
            if config_dict:
                k8s_config.load_kube_config_from_dict(
                    config_dict
                )
                self.client = k8s_client.CoreV1Api()
            elif config_file or not _is_running_in_k8s():
                # See: https://github.com/kubernetes-client/python/blob/master/examples/out_of_cluster_config.py
                k8s_config.load_kube_config(
                    config_file=config_file,
                    context=context,
                    client_configuration=configuration,
                    persist_config=persist_config,
                )
                self.client = k8s_client.CoreV1Api()
            else:
                if configuration:
                    # See: https://github.com/kubernetes-client/python/blob/master/examples/multiple_clusters.py
                    self.client = k8s_client.CoreV1Api(
                        api_client=k8s_client.ApiClient(configuration))
                else:
                    # See: https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py
                    k8s_config.load_incluster_config()
                    self.client = k8s_client.CoreV1Api()
        except ConfigException as e:
            raise e


    def check_ns_exists(self, namespace):
        '''Check if the specified namespace existing.'''
        ns_list = self.client.list_namespace()

        ns_name_list = [ns.metadata.name for ns in ns_list.items]

        if namespace in ns_name_list:
            return True
        else:
            return False


    def create_namespace(
            self,
            name: str,
            labels: Dict[str, str]=None,
            annotations: Dict[str, str]=None,
            timeout_seconds=30,
            ):
        body = V1Namespace(
            metadata=V1ObjectMeta(
                name=name,
                labels=labels,
                annotations=annotations,
            ),
        )
        self.client.create_namespace(body)

        self.client.create_service_account()
    
        start = time.time()
        delta = time.time() - start
        created = False
        while not created and delta < timeout_seconds:
            time.sleep(2)
            created = self.check_ns_exists(namespace=name)
            delta = time.time() - start
    
        if created:
            ns = self.client.read_namespace(name=name)
        else:
            raise KubernetesActionException(ResponseCode.NAMESPACE_NOT_FOUND)

    def patch_namespace(
            self,
            name: str,
            labels: Dict[str, str]=None,
            annotations: Dict[str, str]=None,
            ):
        ns: V1Namespace = self.client.read_namespace(name=name)

        old_metadata: V1ObjectMeta = ns["metadata"]
        old_labels = old_metadata["labels"]
        old_annotations = old_metadata["annotations"]
        new_labels = dict(old_labels, **labels)
        new_annotations = dict(old_annotations, **annotations)
        new_ns = V1Namespace(
            metadata=V1ObjectMeta(
                name=name,
                labels=new_labels,
                annotations=new_annotations,
            ),
        )
        return self.client.patch_namespace(name=name, body=new_ns)


    def prepare_namespace(
            self,
            name: str,
            project_id: int,
            labels: Dict[str, str] = None,
            annotations: Dict[str, str] = None,
            timeout_seconds=30,
            use_ns_nodeselector: bool = False,
    ):
        if labels:
            labels["istio-injection"] = "enabled"
            labels["runtime/project-id"] = str(project_id)
        else:
            labels = {
                "istio-injection": "enabled",
                "runtime/project-id": str(project_id),
            }
        # if self.check_ns_exists(namespace=name):
        #     namespace = self.client.read_namespace(name=name)
        #     old_labels = namespace["metadata"]["labels"]
        #     namespace["metadata"]["labels"] = old_labels | labels

        if use_ns_nodeselector:
            ns_annotations = {
                "scheduler.alpha.kubernetes.io/node-selector": "app/group=aiip-runtime,app/inferencespace=true"}
            if annotations:
                # annotations |= default_annotations
                annotations = dict(ns_annotations, **annotations)

        if self.check_ns_exists(namespace=name):
            old_ns: V1Namespace = self.client.read_namespace(name=name)
            old_metadata: V1ObjectMeta = old_ns.metadata
            old_metadata.labels = dict(old_metadata.labels, **labels)
            if annotations:
                old_metadata.annotations = dict(old_metadata.annotations, **annotations)
            old_ns.metadata = old_metadata

            new_ns = self.client.patch_namespace(name=name, body=old_ns)
        else:
            body = V1Namespace(
                metadata=V1ObjectMeta(
                    name=name,
                    labels=labels,
                    annotations=annotations,
                ),
            )
            new_ns = self.client.create_namespace(body)

        return new_ns

    # def create_namespaced_secret_dockerconfig(self,
    #         namespace="default",
    #         metadata=metadata,
    #         data=None,
    #         string_data=None,
    #         ):
        
    #     self.client.create_namespaced_secret(
    #         namespace=namespace,
    #         body=V1Secret(
    #             api_version=k8s_client,
    #             kind=None,
    #             metadata=Metadata
    #             type=type,
    #             data=data,
    #             string_data=string_data,
    #         )
    #     )

    def prepare_ns_resource_management(self, namespace):

        items = V1LimitRangeItem(
            type="Container",
            default=dict(cpu="25m", memory="50Mi"),
        )

        body = V1LimitRange(
            # metadata=V1ObjectMeta(
            #     name=namespace + "_limit_range",
            # ),
            # spec=V1LimitRangeSpec(limits=V1LimitRangeList(items = cpu))
            spec=V1LimitRangeSpec(limits=[items])
        )

        self.client.create_namespaced_limit_range(namespace, body)


    def create_secret(
            self,
            name,
            namespace: str = "default",
            type="Opaque",
            labels=None,
            annotations=None,
            data=None,
            string_data=None
            ) -> V1Secret:
        'Create namespaced secret, and return the secret name.'
        try:
            created_secret = self.client.create_namespaced_secret(
                namespace,
                V1Secret(
                    api_version='v1',
                    kind='Secret',
                    metadata=V1ObjectMeta(
                        name=name,
                        annotations=annotations,
                        labels=labels),
                    type=type,  # "kubernetes.io/dockerconfigjson", "kubernetes.io/basic-auth"
                    data=data,
                    string_data=string_data))
        except ApiException as e:
            raise RuntimeError(
                "Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % e)

        return created_secret

    def patch_secret(
            self,
            name,
            namespace: str = "default",
            type="Opaque",
            labels=None,
            annotations=None,
            data=None,
            string_data=None
            ) -> V1Secret:
        'Create namespaced secret, and return the secret name.'
        try:
            created_secret = self.client.patch_namespaced_secret(
                name,
                namespace,
                V1Secret(
                    api_version='v1',
                    kind='Secret',
                    metadata=V1ObjectMeta(
                        name=name,
                        annotations=annotations,
                        labels=labels),
                    type=type,  # "kubernetes.io/dockerconfigjson", "kubernetes.io/basic-auth"
                    data=data,
                    string_data=string_data
                ))
        except ApiException as e:
            raise RuntimeError(
                "Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % e)

        return created_secret

    def prepare_secret(
            self,
            name,
            namespace: str = "default",
            type="Opaque",
            labels=None,
            annotations=None,
            data=None,
            string_data=None
            ) -> V1Secret:
        '''Set secret, create if secret does not exist, otherwise patch it.'''
        if self.check_secret_exists(namespace, secret_name=name):
            return self.patch_secret(
                namespace,
                name=name,
                type=type,
                labels=labels,
                annotations=annotations,
                data=data,
                string_data=string_data,
            )
        else:
            return self.create_secret(
                namespace,
                name=name,
                type=type,
                labels=labels,
                annotations=annotations,
                data=data,
                string_data=string_data,
            )

    def create_opaque_secret(
            self,
            name,
            namespace: str = "default",
            labels=None,
            annotations=None,
            data=None,
            string_data=None
            ) -> V1Secret:
        return self.prepare_secret(
            namespace,
            name=name,
            type="Opaque",
            labels=labels,
            annotations=annotations,
            # data=data,
            string_data=string_data,
        )


    def create_dockerconfig_secret(
            self,
            name,
            namespace: str = "default",
            labels=None, annotations=None,
            domain: str = None,
            username: str = None,
            password: str = None
            ) -> V1Secret:
        config = {
            "auths": {
                domain: {
                    "username": username,
                    "password": password,
                    "auth": self.encode_b64(f"{username}:{password}")
                }
            }
        }
        return self.set_secret(
            namespace,
            name=name,
            type="kubernetes.io/dockerconfigjson",
            labels=labels,
            annotations=annotations,
            string_data={".dockerconfigjson": json.dumps(config)},
        )


    def create_image_pull_secrets(self,
                                  namespace,
                                  name,
                                  labels=None,
                                  domain=None,
                                  username=None,
                                  password=None,
                                  ):
        image_pull_secret_name = self.create_dockerconfig_secret(
            namespace=namespace,
            name=name,
            labels=labels,
            domain=str(domain),
            username=str(username),
            password=str(password),
        )
        return image_pull_secret_name


    def create_basic_auth_secret(self,
                                 namespace, name=None,
                                 labels=None, annotations=None, username=None, password=None):
        'Create namespaced secret, and return the secret name.'
        try:
            return self.set_secret(
                namespace,
                name=name,
                type="kubernetes.io/basic-auth",
                labels=labels,
                annotations=annotations,
                string_data={"username": username, "password": password},
            )
        except ApiException as e:
            raise RuntimeError(
                "Exception when calling CoreV1Api->create_namespaced_secret: %s\n" % e)


    def create_service_account(self,
                               namespace, sa_name,
                               labels=None, secret_name=None,
                               image_pull_secret_name=None
                               ):
        'Create namespaced service account, and return the service account name'
        try:
            self.client.create_namespaced_service_account(
                namespace,
                V1ServiceAccount(
                    metadata=V1ObjectMeta(
                        name=sa_name,
                        labels=labels,
                    ),
                    secrets=[V1ObjectReference(
                        name=secret_name)],
                    image_pull_secrets=[V1LocalObjectReference(
                        name=image_pull_secret_name)]
                )
            )
        except ApiException as e:
            raise RuntimeError(
                "Exception when calling CoreV1Api->create_namespaced_service_account: %s\n" % e)

        # logger.info('Created Service account: %s in namespace %s',
        #             sa_name, namespace)

    def patch_service_account(self,
                              namespace, sa_name,
                              labels=None, secret_name=None,
                              image_pull_secret_name=None
                              ):
        'Patch namespaced service account to attach with created secret.'
        try:
            self.client.patch_namespaced_service_account(
                sa_name,
                namespace,
                V1ServiceAccount(
                    metadata=V1ObjectMeta(
                        name=sa_name,
                        labels=labels,
                    ),
                    secrets=[V1ObjectReference(
                        name=secret_name)],
                    image_pull_secrets=[V1LocalObjectReference(
                        name=image_pull_secret_name)]
                )
            )
        except ApiException as e:
            raise RuntimeError(
                "Exception when calling CoreV1Api->patch_namespaced_service_account: %s\n" % e)


    def prepare_service_account(self, namespace, service_account_name, labels=None, secret_name=None,
                            image_pull_secret_name=None):
        '''Set service account, create if service_account does not exist, otherwise patch it.'''
        if self.check_sa_exists(namespace=namespace, service_account_name=service_account_name):
            self.patch_service_account(
                namespace=namespace,
                sa_name=service_account_name,
                labels=labels,
                secret_name=secret_name,
                image_pull_secret_name=image_pull_secret_name,
            )
        else:
            self.create_service_account(
                namespace=namespace,
                sa_name=service_account_name,
                labels=labels,
                secret_name=secret_name,
                image_pull_secret_name=image_pull_secret_name,
            )

    def build_resource_spec(
            self,
            cpu_req: Optional[float] = None,
            cpu_limit: Optional[float] = None,
            mem_req: Optional[int] = None,
            mem_limit: Optional[int] = None,
            gpu_req: Optional[int] = None,
            gpu_limit: Optional[int] = None,
            ) -> V1ResourceRequirements:
        return V1ResourceRequirements(
            requests=Spec(
                cpu=cpu_req,
                memory=mem_req,
                gpu=gpu_req,
            ).dict(),
            limits=Spec(
                cpu=cpu_limit,
                memory=mem_limit,
                gpu=gpu_limit,
            ).dict(),
        )

    @staticmethod
    def encode_b64(s: str) -> str:
        return base64.b64encode(s.encode()).decode()

    @staticmethod
    def decode_b64(s: str) -> str:
        return base64.b64decode(s.encode()).decode()

__author__ = 'sarvesh.singh'

import time
import kubernetes
from test_utils.logger import Logger


class K8:
    """
    Class for Kubernetes !!
    """

    def __init__(self):
        """
        Connect to K8 Cluster
        """
        self.logger = Logger(name='K8').get_logger
        self.logger.debug('Connecting to k8 !!')

        # Load kube Config
        kubernetes.config.load_kube_config()
        self.client = kubernetes.client.CoreV1Api()
        self.watch = kubernetes.watch.Watch()
        self.params = {'pretty': 'pretty_example'}

    def list_namespaces(self):
        """
        Get all namespaces
        """
        return self.client.list_namespace()

    def get_namespace(self, namespace=None):
        """
        Get namespace
        :param namespace: Namespace from which pods to be fetched
        """
        _namespace = self.client.read_namespace(name=namespace)
        return _namespace

    def get_all_pods(self, namespace=None, fetch_all=False):
        """
        Get all Pods in a namespace
        :param namespace: Namespace from which pods to be fetched
        :param fetch_all: Fetch all Pods, even Scaled and Stopped Ones
        :return:
        """
        _pods = []
        for _pod in self.client.list_namespaced_pod(namespace=namespace).items:
            if fetch_all:
                _pods.append(_pod.metadata.name)
            else:
                if _pod.status.phase in ['Running', 'Succeeded'] and len(
                        [x for x in _pod.status.conditions if x.status == 'False']) == 0:
                    _pods.append(_pod.metadata.name)
                else:
                    self.logger.debug(
                        f'{namespace} Pod {_pod.metadata.name} is in {_pod.status.phase} !!')

        if len(_pods) == 0:
            raise Exception(f'Found Zero Pods for {namespace}- namespace !!')

        return _pods

    def get_all_services(self, namespace=None):
        """
        Get all Services in a namespace
        :param namespace: Namespace from which pods to be fetched
        :return:
        """
        _services = []
        for _service in self.client.list_namespaced_service(namespace=namespace).items:
            _services.append(_service.metadata.name)

        if len(_services) == 0:
            raise Exception(f'Found Zero Services for {namespace}- namespace !!')

        return _services

    def get_logs_for_pod(self, namespace=None, pod_name=None, duration=None):
        """
        Get Logs for a given Pod
        :param namespace:
        :param pod_name:
        :param duration:
        :return:
        """
        if duration:
            self.params['since_seconds'] = str(duration)

        try:
            logs = self.client.read_namespaced_pod_log(pod_name, namespace, **self.params)
        except (Exception, KeyError, ValueError):
            self.logger.error(f'Failed to Get Pod: {pod_name} Logs !!')
            return []

        return logs

    def describe_pod(self, pod_name=None, namespace=None):
        """
        Describe a Name-spaced Pod
        :param pod_name: Pod from which info needs to be fetched
        :param namespace: Namespace from which pods to be fetched
        """
        _namespace = self.client.read_namespaced_pod(name=pod_name, namespace=namespace)
        return _namespace

    def delete_pod(self, namespace=None, pod_name=None):
        """
        Delete a Name-spaced Pod
        :param namespace:
        :param pod_name:
        """
        self.client.delete_namespaced_pod(name=pod_name, namespace=namespace)
        for event in self.watch.stream(func=self.client.list_namespaced_pod, namespace=namespace):
            # event.type: ADDED, MODIFIED, DELETED
            if event["type"] == "DELETED":
                self.watch.stop()
                time.sleep(3)
                return

    def delete_namespace(self, namespace=None):
        """
        Delete a Namespace
        :param namespace:
        """
        try:
            self.client.delete_namespace(name=namespace)
        except BaseException as ex:
            if ex.reason == 'Not Found':
                self.logger.info(f'Env: {namespace} does not exist !!')
            else:
                raise Exception(f'Env: {namespace} did not get deleted !! ERR: {ex}')

import os
from unittest import TestCase

from kubernetes import config

from pbsrollout.k8s_utils import import_kube_config
from pbsrollout.process_cluster import remove_old_pods


class Test(TestCase):
    def test_remove_old_pods(self):
        path = os.environ['GOPATH'] + '/src/github.com/publica-project/prebid-kube-manifests/aws.us-east-1-eks-23-v3'
        api_client = config.new_client_from_config(config_file=import_kube_config(path + '/.k8s-assets/kubeconfig'))

        err = remove_old_pods('tesk_k8s', path, api_client)
        self.assertEqual('', err)

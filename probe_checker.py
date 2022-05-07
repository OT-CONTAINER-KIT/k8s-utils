#!/usr/bin/python3
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import config
import argparse


def initiate_api():
    """Function to Initiate Kubernetes API"""
    configuration = config.load_kube_config()
    api_instance = kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(configuration))
    return api_instance

def list_probe(namespace):
    """Function to list the probes of different namespaces"""
    try:
        api_instance = initiate_api()
        namespaces = api_instance.list_namespaced_deployment(namespace).items
        for namespace in namespaces:
            http_info = namespace.spec.template.spec.containers[0].liveness_probe
            if http_info is not None:
                if http_info.http_get is not None:
                    print(namespace.metadata.name, http_info.http_get.path)
                else:
                    print(namespace.metadata.name, "NoHealthcheckConfigured")
            else:
                print(namespace.metadata.name, "NoHealthcheckConfigured")
    except ApiException as e:
        print("Exception when calling AppsV1Api->list_namespaced_deployment: %s\n" % e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--namespace', type=str, help="Name of the namespace for probe info")
    args = parser.parse_args()
    if args.namespace is None:
        parser.print_help()
    else:
        list_probe(args.namespace)

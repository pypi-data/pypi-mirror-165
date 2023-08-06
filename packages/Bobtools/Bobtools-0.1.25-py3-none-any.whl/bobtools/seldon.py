
try:
    from kubernetes import client, config
except:
    None

class SeldonApi:
    def __init__(self):
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()
        self.custom_object_api = client.CustomObjectsApi()


    def get_deployment(self, name, namespace = 'seldon'):
        try: 
            resource = self.custom_object_api.get_namespaced_custom_object(name=name, namespace=namespace,
                group="machinelearning.seldon.io", version="v1", plural="seldondeployments")
            return resource
        except:
            return None

    def get_deployment_exists(self, name, namespace = 'seldon'):
        try: 
            resource = self.custom_object_api.get_namespaced_custom_object(name=name, namespace=namespace,
                group="machinelearning.seldon.io", version="v1", plural="seldondeployments")
            return True
        except:
            return False

    def create_deployment(self, template_name, namespace = 'seldon'):
        with open("deploy.yaml", 'rb') as f:
            template = yaml.load(f)
            name = template['metadata']['name']
            if self.get_deployment_exists(name): self.delete_deployment(name)

            response = self.custom_object_api.create_namespaced_custom_object(namespace=namespace,
                group="machinelearning.seldon.io", version="v1", plural="seldondeployments",
                body=template)
        return response

    def delete_deployment(self, name, namespace = 'seldon'):
        try: 
            resource = self.custom_object_api.delete_namespaced_custom_object(name=name, namespace=namespace,
                group="machinelearning.seldon.io", version="v1", plural="seldondeployments",
            body=client.V1DeleteOptions())
            return resource
        except:
            pass

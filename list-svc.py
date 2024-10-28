import yaml
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Initialize Kubernetes API client
v1 = client.CoreV1Api()

# Get all services in all namespaces
services = v1.list_service_for_all_namespaces()

# Prepare the data structure for checks.yaml
checks_data = []

for svc in services.items:
    namespace = svc.metadata.namespace
    svc_name = svc.metadata.name

    # Skip services with names containing '-svc' or 'kfp'
    if '-svc' in svc_name or 'kfp' in svc_name:
        continue

    # Skip services with ownerReferences of kind 'Notebook'
    if svc.metadata.owner_references:
        if any(owner.kind == 'Notebook' for owner in svc.metadata.owner_references):
            continue

    ports = svc.spec.ports
    if ports:  # Check if ports is not None
        for port in ports:
            port_number = port.port
            check_entry = {
                'title': namespace,
                'checks': [
                    {
                        'name': svc_name,
                        'type': 'http',
                        'host': f'http://{svc_name}:{port_number}/',
                        'url': f'http://{svc_name}:{port_number}/',
                        'expected_code': 200
                    }
                ]
            }
            checks_data.append(check_entry)

# Write the data to checks.yaml
with open('checks.yaml', 'w') as file:
    yaml.dump(checks_data, file, default_flow_style=False)
# TARGER: Neural Argument Mining at Your Fingertips

Helm chart for installing Targer on a Kubernetes cluster.

## Deployment

1. Install [Helm](https://helm.sh/docs/intro/quickstart/) and configure `kubectl` for your cluster.
2. Generate Kubernetes templates for manual error checking:
    
    ```shell script
    helm template targer targer 
    ```
    
    This step can be skipped, but the generated template gives you a good preview what will be deployed in the next step.
3. Deploy to Kubernetes cluster:

    ```shell script
    helm install targer targer 
    ```
    
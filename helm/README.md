# TARGER: Neural Argument Mining at Your Fingertips

Helm chart for installing Targer on a Kubernetes cluster.

In the following commands `NAME` is the release name. That name is used for naming Pods, Volumes etc. A Kubernetes namespace may be configured in `NAMESPACE`. Skip the `-n NAMESPACE` option to deploy to the default namespace.

## Deployment

1. Install [Helm](https://helm.sh/docs/intro/quickstart/) and configure `kubectl` for your cluster.
2. Generate Kubernetes templates for manual error checking:
    
    ```shell script
    helm -n NAMESPACE template NAME targer 
    ```
    
    This step can be skipped, but the generated template gives you a good preview what will be deployed in the next step.
3. Deploy to Kubernetes cluster:

    ```shell script
    helm -n NAMESPACE install NAME targer 
    ```

4. If you have previously deployed TARGER to your Kubernetes cluster, you can upgrade the release:

    ```shell script
    helm -n NAMESPACE upgrade NAME targer 
    ```
    
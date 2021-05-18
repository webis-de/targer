# TARGER: Neural Argument Mining at Your Fingertips

Helm chart for installing Targer on a Kubernetes cluster.

## Deployment

1. Install [Helm](https://helm.sh/docs/intro/quickstart/) and configure `kubectl` for your cluster.
2. Generate Kubernetes templates for manual error checking:
    
    ```shell script
    helm template NAME targer 
    ```
    
    This step can be skipped, but the generated template gives you a good preview what will be deployed in the next step.
3. Deploy to Kubernetes cluster:

    ```shell script
    helm install NAME targer 
    ```

4. If you have previously deployed TARGER to your Kubernetes cluster, you can upgrade the release:

    ```shell script
    helm upgrade NAME targer
    ```

   When upgrading, existing Kubernetes resources will be replaced by the new resources.

## Configuration

In the previous commands, `NAME` is the release name. That name is used for naming Pods, Volumes etc.

Additionally, when deploying with Helm, the following CLI options can be used to configure the namespace and Elasticsearch login credentials:

- `--set namespace=EXAMPLE` to deploy to the `EXAMPLE` namespace.
- `--set elasticsearch.username=EXAMPLE` to login to Elasticsearch with username `EXAMPLE`.
- `--set elasticsearch.password=EXAMPLE` to login to Elasticsearch with password `EXAMPLE`.

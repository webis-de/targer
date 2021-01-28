# Installation guide

TARGER can be installed in two ways, either manually or with prebuilt Docker containers.

## Prerequisites

For installing TARGER, we recommend using Python 3.5.

## General

The models for the backend are not included and must be manually downloaded.
Instructions and URLs can be found in the project [readme](../README.md#quick-setup-with-docker).

Now clone this repository and open the cloned directory:

```shell
git clone https://github.com/webis-de/targer && cd targer
```

## Manual installation

Manual installation can be structured in the different parts of the [system architecture](system-architecture.md).
Each part can be installed individually and on different machines.

### Setup backend

_Hint: this document describes the same setup as the backend [`Dockerfile`](../backend/Dockerfile)._

1. Go to backend directory:

    ```shell
    cd backend
    ```

1. Clone the [BiLSTM-CNN-CRF](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf) repository:

    ```shell
    git clone https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf
    ```

1. Install required Python packages:

    ```shell
    pip install -r emnlp2017-bilstm-cnn-crf/requirements.txt -r requirements.txt
    ```

1. Move Phyton source code into the cloned directory:

    ```shell
    mv backend.py Model.py ModelNewES.py ModelNewWD.py emnlp2017-bilstm-cnn-crf/
    mv BiLSTM.py emnlp2017-bilstm-cnn-crf/neuralnets/
    ```

1. Move configuration into the cloned directory:

    ```shell
    mv config.ini emnlp2017-bilstm-cnn-crf/
    ```

1. Move downloaded models into the cloned directory:

    ```shell
    mv models/*.h5 emnlp2017-bilstm-cnn-crf/models/
    ```

1. Go to the cloned directory:

    ```shell
    cd emnlp2017-bilstm-cnn-crf
    ```

1. Run the server in developement mode:

    ```shell
    python backend.py
    ```

    Alternatively, you can use the backend with a Nginx web server and WSGI.
    Use the included `uwsgi.ini` to load it in the environment.

### Setup frontend

1. Go to frontend directory:

    ```shell
    cd frontend
    ```

1. Edit the Backend URLs in `config.ini`.
    Replace it with the backend server hostname.
    If it runs on the same machine, you can use `localhost`.
1. Install required Python packages:

    ```shell
    pip install -r requirements.txt
    ```

1. Run the server:  
    - In development mode:

        ```shell
        python frontend.py
        ```

    - With Nginx web server and WSGI, you can use the included `uwsgi.ini` to load it in the environment.

### Setup Elasticsearch indexing

1. Install and run [Elasticsearch](https://www.elastic.co/elasticsearch/)
1. Go to batch processing directory:

    ```shell
    cd batch_processing
    ```

1. Install required Python packages:

    ```shell
    pip install -r requirements.txt
    ```

1. Run indexing:

    ```shell
    python index.py -host HOST -port PORT -index INDEX -input FILE
    ```

### Setup batch processing

1. Go to batch processing directory:

    ```shell
    cd batch_processing
    ```

1. Install required Python packages:

    ```shell
    pip install -r requirements.txt
    ```

1. Run argument labelling:

    ```shell
    python label_mp.py --model MODEL --workers N --input FILE --output FILE
    ```

## Docker installation

After cloning the repository, the system can be installed and started with Docker Compose in the default configuration:

```shell
docker-compose up
```

Each part can also be launched individually with their respective `Dockerfile`.

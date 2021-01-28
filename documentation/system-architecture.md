# System architecture

TARGER consists from three different parts:

* Frontend
* Backend
* Batch processing (building the search index)

## Frontend

The frontend is a webserver built with the [Flask](https://palletsprojects.com/p/flask/) framework, to use the argument search engine with a web browser.

## Backend

The backend contains logic for argument classification and generating the annotated results.
It exposes a REST-like API which is used by the frontend.
The backend depends on the [BiLSTM-CNN-CRF](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf) architecture for sequence tagging.
A [Swagger](https://swagger.io/) API interface allows for quickly testing annotation and documents the API.

### Reverse proxy

Both backend and frontend can run behind a reverse proxy like [Nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) or [Apache 2](https://httpd.apache.org/docs/current/howto/reverse_proxy.html).
However, you must configure the reverse proxy to forward the original address and some additional headers.
If you don't specify `X-Script-Name`, the backend will confuse API endpoints and Swagger won't work.

<details>
<summary><strong>Nginx</strong> configuration</summary>

```apacheconf
location /subdir {
    proxy_pass http://HOSTNAME:PORT;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Script-Name /subdir;
}
```

</details>

<details>
<summary><strong>Apache 2</strong> configuration</summary>

```apacheconf
<Location /subdir>
    Header add X-Script-Name "/subdir"
    RequestHeader set X-Script-Name "/subdir"
    
    ProxyPass http://HOSTNAME:PORT
    ProxyPassReverse http://HOSTNAME:PORT
</Location>
```

</details>

## Batch processing

The batch processing module provides scripts for argument labeling and indexing to [Elasticsearch](https://www.elastic.co/de/elasticsearch/).

### Argument labeling

Data is being parsed and labeled by applying the model in a parallel way.

### Elasticsearch indexing

Data produced by argument labeling is being parsed and saved to the ES index.

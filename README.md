[![GitHub Actions](https://img.shields.io/github/workflow/status/webis-de/targer/Docker%20build?style=flat-square)](https://github.com/webis-de/targer/actions?query=workflow%3A%22Docker+build%22)
[![Docker Hub frontend tags](https://img.shields.io/docker/v/webis/targer-frontend?style=flat-square&label=frontend+version)](https://hub.docker.com/repository/docker/webis/targer-frontend/tags)
[![Docker Hub frontend](https://img.shields.io/docker/pulls/webis/targer-frontend?style=flat-square&label=frontend+pulls)](https://hub.docker.com/repository/docker/webis/targer-frontend)
[![Docker Hub backend tags](https://img.shields.io/docker/v/webis/targer-backend?style=flat-square&label=backend+version)](https://hub.docker.com/repository/docker/webis/targer-backend/tags)
[![Docker Hub backend](https://img.shields.io/docker/pulls/webis/targer-backend?style=flat-square&label=backend+pulls)](https://hub.docker.com/repository/docker/webis/targer-backend)

# TARGER: Neural Argument Mining at Your Fingertips

This page contains code of the web application and web service based on the neural [argument tagger](http://github.com/achernodub/targer).
You can enter some text in the input box and detect arguments in it with one of the pre-trained neural models for argument mining. 

More specifically, this repository shares code and data related to the following demo paper:  
*Artem Chernodub, Oleksiy Oliynyk, Philipp Heidenreich, Alexander Bondarenko, Matthias Hagen, 
Chris Biemann, and Alexander Panchenko (2019):
[TARGER: Neural Argument Mining at Your Fingertips](https://webis.de/publications.html#bondarenko_2019b). 
In Proceedings of the 57th Annual Meeting of the Association of Computational Linguistics (ACL 2019). Florence, Italy.*

If you use the demo or would like to refer to it, please cite the paper mentioned above. 
You can use the following BibTeX information for citation: 

```bibtex
@inproceedings{chernodub2019targer,
  title     = {TARGER: Neural Argument Mining at Your Fingertips},
  author    = {Chernodub, Artem and Oliynyk, Oleksiy and Heidenreich, Philipp and Bondarenko, Alexander and 
               Hagen, Matthias and Biemann, Chris  and Panchenko, Alexander},
  booktitle = {Proceedings of the 57th Annual Meeting of the Association of Computational Linguistics (ACL'2019)},
  year      = {2019},
  address   = {Florence, Italy}
}
```

Below you will find instructions on how to run the TARGER web application and its API locally (using Docker).
Alternatively you can just access the [online demo](https://demo.webis.de/targer) though web interface or using API. 

The web application relies on a [neural tagging library](http://github.com/achernodub/targer) based on the [PyTorch](https://pytorch.org) framework. 
You may also find this library useful on its own, e.g., for training sequence taggers for argument mining, part of speech tagging, or named entity recognition.
The library is taking CoNLL files as input, is easy to use, and has a minimal number of dependencies.
Though the library lives in a separate repository, it is also part of the TARGER project.
So if you are using the library, please also cite the paper mentioned above.
For detailed documentation about the tagging library refer to [its repository](http://github.com/achernodub/targer).

## Quick setup with Docker

1. Clone this repository:

    ```shell script
    git clone https://github.com/webis-de/targer && cd targer
    ```

1. Download [pre-trained model files](https://files.webis.de/data-in-production/data-research/acqua/targer/models/) to the `models` directory:

    ```shell script
    wget https://files.webis.de/data-in-production/data-research/acqua/targer/models/ \
      --recursive --level=1 \
      --no-directories --no-host-directories \
      --accept=h5,hdf5 --directory-prefix=models
    ```

1. Run the demo using Docker:

    ```shell script
    docker-compose up
    ```

1. Access the frontend at [localhost:6001](http://localhost:6001) and the backend REST-like API at [localhost:6000](http://localhost:6000).

## Documentation

Here you can find more detailed documentation of the system architecture, installation, and usage:

* [System architecture](documentation/system-architecture.md)
* [Installation guide](documentation/installation-guide.md)
* [User guide](documentation/user-guide.md)

## License

This repository is released under the  the [MIT license](LICENSE).

Code in this repository is based on [uhh-lt/targer](https://github.com/uhh-lt/targer) and parts of the frontend are based on [displacy-ent](https://github.com/explosion/displacy-ent), both are licensed under the MIT license. 

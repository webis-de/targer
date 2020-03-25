# TARGER: Neural Argument Mining at Your Fingertips

This page contains code of the Web application and web service 
based on the neural [argument tagger](http://github.com/achernodub/bilstm-cnn-crf-tagger).
The figure below illustrates how the sytem looks like: 
you can enter some text in the input box and detect arguments in it 
with one of the pre-trained neural models for argument mining. 

**The front-end code is based on MIT licensed [displacy-ent](https://github.com/explosion/displacy-ent) 
by [ExplosionAI](http://explosion.ai). We are thankful to [Ines Motani](https://github.com/ines) 
for developing this piece of software and making it publicly available under the MIT license.** 

More specifically, this repository shares code and data related to the following demo paper:

*Artem Chernodub, Oleksiy Oliynyk, Philipp Heidenreich, Alexander Bondarenko, Matthias Hagen, 
Chris Biemann, and Alexander Panchenko (2019):
[TARGER: Neural Argument Mining at Your Fingertips](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2019-chernodubetal-acl19demo-targer.pdf). 
In Proceedings of the 57th Annual Meeting of the Association of Computational Linguistics (ACL'2019). Florence, Italy.*

If you use the demo or would like to refer to it, please cite the paper mentioned above. 
You can also use the following BibTeX information for citation: 

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

Below you will find some instructions on how to run the TARGER web application and its API locally (using docker).
Alternatively you can just [access it online](http://ltdemos.informatik.uni-hamburg.de/targer/) 
though web interface or using API. 
This web application relies on a [neural tagging library](http://github.com/achernodub/targer) 
based on the [PyTorch](https://pytorch.org) framework. 
You may also find this library useful on its own, i.e. for training sequence taggers for argument mining, 
but also for other tasks, such as part of speech tagging or named entity recognition.
The library is taking as input CoNLL files, is easy to use, and has a minimal number of dependencies.
Note that while this library lives in a separate repository from the web application,
it is also part of the TARGER project.
So if you are using the library, please also cite the paper mentioned above.
For detailed documentation about the tagging library refer to [its repository](http://github.com/achernodub/targer).  

## Quick run web application with docker

1. Download all the [pre-trained model files](http://ltdata1.informatik.uni-hamburg.de/targer/)
to the `backend/models` directory:
```shell script
cd backend
wget http://ltdata1.informatik.uni-hamburg.de/targer/COMBO.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/ES.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/ES_dep.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/IBM.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/WD.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/WD_dep.h5
wget http://ltdata1.informatik.uni-hamburg.de/targer/model_new_es.hdf5
wget http://ltdata1.informatik.uni-hamburg.de/targer/model_new_wd.hdf5
```
2. Run the demo using Docker: 
`docker-compose up`
3. Access the frontend at [localhost:6001](http://localhost:6001) 
and the backend REST API at [localhost:6000](http://localhost:6000).

## Documentation

* [System architecture](https://github.com/uhh-lt/argument-search-engine/wiki/System-architecture)
* [Installation guide](https://github.com/uhh-lt/argument-search-engine/wiki/Installation-guide)
* [User guide](https://github.com/uhh-lt/argument-search-engine/wiki/User-guide)

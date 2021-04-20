#!/usr/bin/env python3

from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api, Resource
from flask import make_response
import configparser
from flask import jsonify

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
config = config_parser['backend']

"""Models"""

from Model import Model
from ModelNewES import ModelNewES
from ModelNewWD import ModelNewWD

modelNewES = ModelNewES()

modelNewWD = ModelNewWD()

modelIBM = Model("IBM.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelIBM.label("Therefore fixed punishment will")

modelCombo = Model("COMBO.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelCombo.label("Therefore fixed punishment will")

modelES = Model("ES.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelES.label("Therefore fixed punishment will")

modelWD = Model("WD.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelWD.label("Therefore fixed punishment will")

modelES_dep = Model("ES_dep.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelES_dep.label("Therefore fixed punishment will")

modelWD_dep = Model("WD_dep.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelWD_dep.label("Therefore fixed punishment will")

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')

        if script_name:
            environ['SCRIPT_NAME'] = script_name
            if environ['PATH_INFO'].startswith(script_name):
                environ['PATH_INFO'] = environ['PATH_INFO'][len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config['SWAGGER'] = {
    'title': 'TARGER API',
    'favicon': "https://assets.webis.de/img/favicon.png",
    'uiversion': 3,
}
template = {
    "info": {
        "title": "TARGER API",
        "description": "Demo API for our [ACL 2019 paper](https://doi.org/10.18653/v1/P19-3031):\n"
                       "_TARGER: Neural Argument Mining at Your Fingertips_\n"
                       "\n"
                       "This API serves the TARGER [demo web app](https://demo.webis.de/targer/).",
        "contact": {
            "name": "Webis Group",
            "url": "https://webis.de/",
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        "termsOfService": "https://webis.de/legal.html",
    },
    "externalDocs": {
        "description": "GitHub repository",
        "url": "https://github.com/webis-de/targer",
    },
    "basePath": LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')),
    "swaggerUiPrefix": LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')),
}
Swagger(app, template=template)
api = Api(app)


class ClassifyNewWD(Resource):
    def post(self):
        """
        Tag arguments in free input text (WebD dataset, GloVe embeddings)
        Tag input text with argument structures using [GloVe embeddings](https://doi.org/10.3115/v1/D14-1162) pretrained on the [WebD dataset](https://doi.org/10.1162/COLI_a_00276).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Chernodub et al. (2019)](https://doi.org/10.18653/v1/P19-3031).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelNewWD.label(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyNewPE(Resource):
    def post(self):
        """
        Tag arguments in free input text (Essays dataset, GloVe embeddings)
        Tag input text with argument structures using [GloVe embeddings](https://doi.org/10.3115/v1/D14-1162) pretrained on the [Essays dataset](https://doi.org/10.18653/v1/P17-1002).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Chernodub et al. (2019)](https://doi.org/10.18653/v1/P19-3031).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelNewES.label(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyES(Resource):
    def post(self):
        """
        Tag arguments in free input text (Essays dataset, fastText embeddings)
        Tag input text with argument structures using [fastText embeddings](https://aclweb.org/anthology/L18-1008) pretrained on the [Essays dataset](https://doi.org/10.18653/v1/P17-1002).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Reimers and Gurevych (2017)](https://doi.org/10.18653/v1/D17-1035).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelES.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyWD(Resource):
    def post(self):
        """
        Tag arguments in free input text (WebD dataset, fastText embeddings)
        Tag input text with argument structures using [fastText embeddings](https://aclweb.org/anthology/L18-1008) pretrained on the [WebD dataset](https://doi.org/10.1162/COLI_a_00276).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Reimers and Gurevych (2017)](https://doi.org/10.18653/v1/D17-1035).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelWD.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyES_dep(Resource):
    def post(self):
        """
        Tag arguments in free input text (Essays dataset, dependency-based embeddings)
        Tag input text with argument structures using [dependency-based embeddings](https://doi.org/10.3115/v1/P14-2050) pretrained on the [Essays dataset](https://doi.org/10.18653/v1/P17-1002).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Reimers and Gurevych (2017)](https://doi.org/10.18653/v1/D17-1035).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelES_dep.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyWD_dep(Resource):
    def post(self):
        """
        Tag arguments in free input text (WebD dataset, dependency-based embeddings)
        Tag input text with argument structures using [dependency-based embeddings](https://doi.org/10.3115/v1/P14-2050) pretrained on the [WebD dataset](https://doi.org/10.1162/COLI_a_00276).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Reimers and Gurevych (2017)](https://doi.org/10.18653/v1/D17-1035).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelWD_dep.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyIBM(Resource):
    def post(self):
        """
        Tag arguments in free input text (IBM dataset, fastText embeddings)
        Tag input text with argument structures using [fastText embeddings](https://aclweb.org/anthology/L18-1008) pretrained on the [IBM dataset](https://aclweb.org/anthology/C18-1176).
        This model uses the BiLSTM-CNN-CRF sequence tagger implementation of [Reimers and Gurevych (2017)](https://doi.org/10.18653/v1/D17-1035).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelIBM.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyCombo(Resource):
    def post(self):
        """
        Tag arguments in free input text (Combo model)
        Tag input text with argument structures using the Combo model from [Universität Hamburg](https://github.com/uhh-lt/targer/blob/a2a89ebfb366bc723a38dae963f8cb8b130f7e81/backend/backend.py#L305).
        ---
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelCombo.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class DeprecatedResource(Resource):
    def __init__(self, resource: Resource):
        self.resource = resource

    @property
    def __name__(self):
        return "Deprecated {}".format(self.resource.__name__)

    def post(self):
        """
        Deprecated endpoint.
        This endpoint has been renamed for consistency. Use the updated endpoint instead.
        ---
        deprecated: true
        consumes:
          - text/plain
        parameters:
          - in: body
            name: text
            type: string
            required: true
            description: Text to tag with argument structures.
            example: "Quebecan independence is justified.
                      In the special episode in Japan, his system is restored by a doctor
                      who wishes to use his independence for her selfish reasons."
        responses:
          200:
            description: List of sentences of tokens, annotated with labels.
            schema:
              $ref: "#/definitions/Sentences"
        definitions:
          Sentences:
            type: array
            items:
              $ref: "#/definitions/Sentence"
          Sentence:
            type: array
            items:
              $ref: "#/definitions/Token"
          Token:
            type: object
            required:
              - label
              - prob
              - token
            properties:
              label:
                type: string
                example: "P-I"
              prob:
                type: number
                example: 0.985
              token:
                type: string
                example: "system"
        """
        return self.resource.post()


api.add_resource(ClassifyES_dep, '/tag-essays-dependency')
api.add_resource(ClassifyES, '/tag-essays-fasttext')
api.add_resource(ClassifyNewPE, '/tag-essays-glove')
api.add_resource(ClassifyIBM, '/tag-ibm-fasttext')
api.add_resource(ClassifyWD_dep, '/tag-webd-dependency')
api.add_resource(ClassifyWD, '/tag-webd-fasttext')
api.add_resource(ClassifyNewWD, '/tag-webd-glove')
api.add_resource(ClassifyCombo, '/tag-combo')

api.add_resource(DeprecatedResource(ClassifyES_dep), '/classifyES_dep')
api.add_resource(DeprecatedResource(ClassifyES), '/classifyES')
api.add_resource(DeprecatedResource(ClassifyNewPE), '/classifyNewPE')
api.add_resource(DeprecatedResource(ClassifyIBM), '/classifyIBM')
api.add_resource(DeprecatedResource(ClassifyWD_dep), '/classifyWD_dep')
api.add_resource(DeprecatedResource(ClassifyWD), '/classifyWD')
api.add_resource(DeprecatedResource(ClassifyNewWD), '/classifyNewWD')
api.add_resource(DeprecatedResource(ClassifyCombo), '/classifyCombo')

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.run(host=config["host"], port=int(config["port"]), debug=True)

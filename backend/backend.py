#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api, Resource, reqparse
from flask import make_response
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import json
import configparser
from flask import jsonify
import json

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
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelCombo.label("Therefore fixed punishment will")

modelES = Model("ES.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelES.label("Therefore fixed punishment will")

modelWD = Model("WD.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelWD.label("Therefore fixed punishment will")

modelES_dep = Model("ES_dep.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelES_dep.label("Therefore fixed punishment will")

modelWD_dep = Model("WD_dep.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
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


template = {
    "swaggerUiPrefix": LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')),
    "info": {
        "title": "TARGER API",
        "description": "Neural Argument Mining at Your Fingertips",
        "contact": {
            "responsibleOrganization": "Webis",
            "responsibleDeveloper": "Jan Heinrich Reimer",
            "email": "jan.reimer@student.uni-halle.de",
            "url": "https://webis.de/",
        },
        "termsOfService": "https://webis.de/legal.html",
    },
}
Swagger(app, template=template)
api = Api(app)


class ClassifyNewWD(Resource):
    def post(self):
        """
       Classifies input text to argument structure (Essays model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelNewWD.label(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyNewPE(Resource):
    def post(self):
        """
       Classifies input text to argument structure (Essays model, fasttext embeddings)

       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelNewES.label(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyES(Resource):
    def post(self):
        """
       Classifies input text to argument structure (Essays model, fasttext embeddings)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelES.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyWD(Resource):
    def post(self):
        """
       Classifies input text to argument structure (WebD model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelWD.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyES_dep(Resource):
    def post(self):
        """
       Classifies input text to argument structure (Essays model, dependency based)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelES_dep.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyWD_dep(Resource):
    def post(self):
        """
       Classifies input text to argument structure (WebD model, dependency based)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelWD_dep.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyIBM(Resource):
    def post(self):
        """
       Classifies input text to argument structure (IBM model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelIBM.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


class ClassifyCombo(Resource):
    def post(self):
        """
       Classifies input text to argument structure (Combo model - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
        inputtext = request.get_data().decode('UTF-8')
        result = modelCombo.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


api.add_resource(ClassifyES, '/classifyES')
api.add_resource(ClassifyWD, '/classifyWD')
api.add_resource(ClassifyES_dep, '/classifyES_dep')
api.add_resource(ClassifyWD_dep, '/classifyWD_dep')
api.add_resource(ClassifyIBM, '/classifyIBM')
api.add_resource(ClassifyCombo, '/classifyCombo')
api.add_resource(ClassifyNewPE, '/classifyNewPE')
api.add_resource(ClassifyNewWD, '/classifyNewWD')

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.run(host=config["host"], port=int(config["port"]), debug=True)

#!/usr/bin/env python3
from pathlib import Path
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from flask import make_response
import configparser
from flask import jsonify
import yaml

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
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
modelIBM.label("Therefore fixed punishment will")

modelCombo = Model("COMBO.h5")
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
modelCombo.label("Therefore fixed punishment will")

modelES = Model("ES.h5")
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
modelES.label("Therefore fixed punishment will")

modelWD = Model("WD.h5")
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
modelWD.label("Therefore fixed punishment will")

modelES_dep = Model("ES_dep.h5")
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
modelES_dep.label("Therefore fixed punishment will")

modelWD_dep = Model("WD_dep.h5")
# We must call this cause of a keras bug: https://github.com/keras-team/keras/issues/2397
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

# Load Swagger base spec from YAML file.
schema_dir = Path(__file__).parent / "schema"
with (schema_dir / "base.yml").open("r") as stream:
    template = yaml.safe_load(stream)
# Update with properties only known at runtime.
template.update({
    "basePath": LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')),
    "swaggerUiPrefix": LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')),
})
swagger = Swagger(app, template=template)


@app.route('/tag-webd-glove', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-glove.yml"))
def tag_webd_glove():
    inputtext = request.get_data().decode('UTF-8')
    result = modelNewWD.label(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyNewWD', methods=['POST'])
@app.route('/classifyWDglove', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-glove-deprecated.yml"))
def tag_webd_glove_deprecated():
    return tag_webd_glove()


@app.route('/tag-essays-glove', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-glove.yml"))
def tag_essays_glove():
    inputtext = request.get_data().decode('UTF-8')
    result = modelNewES.label(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyNewPE', methods=['POST'])
@app.route('/classifyPEglove', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-glove-deprecated.yml"))
def tag_essays_glove_deprecated():
    return tag_essays_glove()


@app.route('/tag-essays-fasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-fasttext.yml"))
def tag_essays_fasttext():
    inputtext = request.get_data().decode('UTF-8')
    result = modelES.label_with_probs(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyES', methods=['POST'])
@app.route('/classifyPEfasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-fasttext-deprecated.yml"))
def tag_essays_fasttext_deprecated():
    return tag_essays_fasttext()


@app.route('/tag-webd-fasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-fasttext.yml"))
def tag_webd_fasttext():
        inputtext = request.get_data().decode('UTF-8')
        result = modelWD.label_with_probs(inputtext)
        response = make_response(jsonify(result))
        response.headers['content-type'] = 'application/json'
        return response


@app.route('/classifyWD', methods=['POST'])
@app.route('/classifyWDfasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-fasttext-deprecated.yml"))
def tag_webd_fasttext_deprecated():
    return tag_webd_fasttext()


@app.route('/tag-essays-dependency', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-dependency.yml"))
def tag_essays_dependency():
    inputtext = request.get_data().decode('UTF-8')
    result = modelES_dep.label_with_probs(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyES_dep', methods=['POST'])
@app.route('/classifyPEdep', methods=['POST'])
@swag_from(str(schema_dir / "tag-essays-dependency-deprecated.yml"))
def tag_essays_dependency_deprecated():
    return tag_essays_dependency()


@app.route('/tag-webd-dependency', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-dependency.yml"))
def tag_webd_dependency():
    inputtext = request.get_data().decode('UTF-8')
    result = modelWD_dep.label_with_probs(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyWD_dep', methods=['POST'])
@app.route('/classifyWDdep', methods=['POST'])
@swag_from(str(schema_dir / "tag-webd-dependency-deprecated.yml"))
def tag_webd_dependency_deprecated():
    return tag_webd_dependency()


@app.route('/tag-ibm-fasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-ibm-fasttext.yml"))
def tag_ibm_fasttext():
    inputtext = request.get_data().decode('UTF-8')
    result = modelIBM.label_with_probs(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyIBM', methods=['POST'])
@app.route('/classifyIBMfasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-ibm-fasttext-deprecated.yml"))
def tag_ibm_fasttext_deprecated():
    return tag_ibm_fasttext()


@app.route('/tag-combined-fasttext', methods=['POST'])
@swag_from(str(schema_dir / "tag-combined-fasttext.yml"))
def tag_combined_fasttext():
    inputtext = request.get_data().decode('UTF-8')
    result = modelCombo.label_with_probs(inputtext)
    response = make_response(jsonify(result))
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/classifyCombo', methods=['POST'])
@swag_from(str(schema_dir / "tag-combined-fasttext-deprecated.yml"))
def tag_combined_fasttext_deprecated():
    return tag_combined_fasttext()


app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.run(host=config["host"], port=int(config["port"]), debug=True)

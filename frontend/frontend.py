#!/usr/bin/env python3

"""be.py: Description."""
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api
import json
import sys
import configparser
import urllib.parse

"""Front-End"""
from flask import render_template
from json import JSONDecodeError
import requests
import os
from elasticsearch import Elasticsearch
import re
import json

"""Spacy"""
import spacy

nlp = spacy.load('xx')

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
config = config_parser['frontend']


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

if os.getenv("ES_USERNAME") and os.getenv("ES_PASSWORD"):
    auth = (os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD"))
else:
    auth = None

es = Elasticsearch(
    hosts=[
        {
            "host": config["es_host"],
            "port": int(config["es_port"])
        }
    ],
    http_auth=auth,
    use_ssl=auth is not None,
)

reversed = True

if (reversed):
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    template2 = dict(swaggerUiPrefix=LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))
    swagger = Swagger(app, template=template2)
else:
    swagger = Swagger(app)

api = Api(app)


def create_api_url(endpoint):
    api_endpoint = config["api_endpoint"]
    if not api_endpoint.endswith("/"):
        api_endpoint += "/"
    return api_endpoint + endpoint


class Sender:
    def send(self, text, classifier):

        if classifier == "IBM":
            url = create_api_url("/tag-ibm-fasttext")
        elif classifier == "ES_dep":
            url = create_api_url("/tag-essays-dependency")
        elif classifier == "ES":
            url = create_api_url("/tag-essays-fasttext")
        elif classifier == "NEWPE":
            url = create_api_url("/tag-essays-glove")
        elif classifier == "WD_dep":
            url = create_api_url("/tag-webd-dependency")
        elif classifier == "WD":
            url = create_api_url("/tag-webd-fasttext")
        elif classifier == "NEWWD":
            url = create_api_url("/tag-webd-glove")
        elif classifier == "Combo":
            url = create_api_url("/tag-combined-fasttext")

        try:
            r = requests.post(url, data=text.encode("utf-8"))
            return r.json()
        except JSONDecodeError:
            print("!!!!", len(text), text)
            pass


sender = Sender()


@app.route('/')
def index():
    return render_template('template_main.html', title="Argument Entity Visualizer", page="index",
                           api_url=config["api_url"], source_url=config["source_url"], paper_doi=config["paper_doi"])


@app.route('/search_text', methods=['POST'])
def search_text():
    """
    Search arguments by keywords.
    ---
    parameters:
      - name: query
        in: formData
        type: string
        required: true
        default: death penalty
      - name: confidence
        in: formData
        type: integer
        minimum: 0
        maximum: 100
        default: 90
      - name: where
        in: formData
        type: array
        items:
          type: string
          minItems: 1
          uniqueItems: true
          enum:
          - text
          - premise
          - claim
          - named_entity
        default:
        - text
        - premise
        - claim
        - named_entity
    responses:
      200:
        description: Search snippets annotated with argument labels.
        schema:
          type: array
          items:
            type: object
            properties:
              text_full:
                type: string
              query_positions:
                type: object
                properties:
                  type:
                    type: string
                    enum:
                    - search
                  start:
                    type: integer
                    minimum: 0
                  end:
                    type: integer
                    minimum: 0
              entity_positions:
                type: object
                properties:
                  type:
                    type: string
                  start:
                    type: integer
                    minimum: 0
                  end:
                    type: integer
                    minimum: 0
              arguments_positions:
                type: object
                properties:
                  type:
                    type: string
                    enum:
                    - premise
                    - claim
                  start:
                    type: integer
                    minimum: 0
                  end:
                    type: integer
                    minimum: 0
              url:
                type: string



    """
    text = request.form.get('query')
    confidence = request.form.get('confidence', default=0)
    where_to_seach = request.form.get('where').split(",")  # List like ['premise', 'claim', 'named_entity', 'text']
    return search_in_es(text, where_to_seach, confidence)


@app.route('/label_text', methods=['POST'])
def background_process_arg():
    """
    Tag arguments in free input text.
    ---
    parameters:
      - in: formData
        name: text
        type: string
        default: |
          Quebecan independence is justified. In the special episode in Japan,
          his system is restored by a doctor who wishes to use his independence for her selfish reasons.
      - name: classifier
        in: formData
        type: string
        enum:
        - IBM
        - ES_dep
        - ES
        - NEWPE
        - WD_dep
        - WD
        - NEWWD
        - Combo
    responses:
      200:
        description: Tags with position and type.
        schema:
          type: array
          items:
            type: object
            properties:
              type:
                type: string
                enum:
                - CLAIM
                - PREMISE
                - PERSON
                - PER
                - NORP
                - FACILITY
                - ORG
                - GPE
                - LOC
                - PRODUCT
                - EVENT
                - WORK OF ART
                - LANGUAGE
                - DATE
                - TIME
                - PERCENT
                - MONEY
                - QUANTITY
                - ORDINAL
                - CARDINAL
                - MISC
              start:
                type: integer
                minimum: 0
              end:
                type: integer
                minimum: 0
    """
    text = request.form.get('text')

    data = []

    # Arg-Mining Tags
    classifier = request.form.get('classifier')
    doc = sender.send(text, classifier)
    currentPos = 0
    for sentence in doc:
        for token in sentence:
            start = text.find(token["token"], currentPos)
            end = start + len(token["token"])
            currentPos = end
            currentWord = {}
            currentWord['start'] = start
            currentWord['end'] = end
            currentWord['type'] = token["label"]
            data.append(currentWord)

    data = do_label_arg(data)

    doc = nlp(text)
    for ent in doc.ents:
        entry = {'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
        data.append(entry)

    return json.dumps(data)


def do_label_arg(marks):
    # print("marks:" + str(marks))
    marks_new = []
    for i, item in enumerate(marks):
        # for (var i = 0; i < marks.length; i++):
        if i > 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif marks[i]['type'][0] == "C" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
                # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P":
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif (marks[i]['type'][0] == "C"):
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 == len(marks):
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                mark['end'] = marks[i]['end']
                marks_new.append(mark)
    return marks_new


SEARCH_KEY_PREMISE = 'premise'
SEARCH_KEY_CLAIM = 'claim'
SEARCH_KEY_ENTITY = 'named_entity'
SEARCH_KEY_TEXT = 'text'


def get_search_field(field, query):
    return {
        "match": {
            field: {
                "query": query
            }
        }
    }


def get_nested_search_field(path, field, query):
    return {
        "nested": {
            "path": path,
            "query": {
                "match": {
                    field: {
                        "query": query
                    }
                }
            },
        }
    }


def get_nested_search_field_with_score(path, field, query, score_field, score):
    return {
        "nested": {
            "path": path,
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            field: {
                                "query": query
                            }
                        }
                    },
                    "filter": {
                        "range": {
                            score_field: {
                                "gt": score
                            }
                        }
                    }
                }
            }
        }
    }


def get_search_element(category, query, confidence):
    if category == SEARCH_KEY_TEXT:
        return get_search_field("sentences.text", query)
    elif category == SEARCH_KEY_PREMISE:
        return get_nested_search_field_with_score(
            "sentences.premises",
            "sentences.premises.text",
            query,
            "sentences.premises.score",
            float(confidence) / 100
        )
    elif category == SEARCH_KEY_CLAIM:
        return get_nested_search_field_with_score(
            "sentences.claims",
            "sentences.claims.text",
            query,
            "sentences.claims.score",
            float(confidence) / 100
        )
    elif category == SEARCH_KEY_ENTITY:
        get_nested_search_field("sentences.entities", "sentences.entities.text", query)


number_of_sentences_around = 3


def search_in_es(query, where_to_search, confidence):
    docs = []
    search_query = query

    if len(where_to_search) == 0:
        where_to_search = [SEARCH_KEY_TEXT]
    where_to_search = set(where_to_search)
    search_elements = [
        get_search_element(search_category, search_query, confidence)
        for search_category in where_to_search
    ]

    if len(search_elements) == 0:
        search_elements.append(get_search_field("sentences.text", search_query))

    body = {
        "size": 25,
        "_source": {
            "includes": [
                "url",
                "sentences.text",
                "sentences.claims.score",
                "sentences.claims.text",
                "sentences.premises.score",
                "sentences.premises.text",
                "sentences.entities.class",
                "sentences.entities.text"
            ]
        },
        "query": {
            "nested": {
                "inner_hits": {
                    "_source": False,
                    "size": 1
                },
                "path": "sentences",
                "query": {
                    "bool": {
                        "should": search_elements
                    }
                }
            }
        }
    }

    res = es.search(
        index=config["es_index"],
        request_timeout=60,
        timeout="1m",
        body=body,
    )

    query_words = search_query.strip().split()
    app.logger.debug(
        "Got %s%s Hits:",
        "≥" if res["hits"]["total"]["relation"] == "gte" else "",
        res['hits']['total']['value']
    )
    app.logger.debug('%s returned hits', len(res['hits']['hits']))

    for hit in res['hits']['hits']:
        doc = {}
        text_full = ""
        arguments_positions = []
        entity_positions = []
        query_search_positions = []

        sentences = hit["_source"]["sentences"]

        index_with_top_match = hit["inner_hits"]["sentences"]["hits"]["hits"][0]["_nested"]["offset"]

        # finding for sentences indexes to show
        if index_with_top_match is None:
            # first sentences
            min_pos = 0
            max_pos = number_of_sentences_around * 2
        elif len(sentences) < 2 * number_of_sentences_around + 1:
            # all sentences
            min_pos = 0
            max_pos = len(sentences) - 1
        elif index_with_top_match < number_of_sentences_around:
            # first sentences
            min_pos = 0
            max_pos = number_of_sentences_around * 2
        elif index_with_top_match > (len(sentences) - 1 - number_of_sentences_around):
            # last sentences
            min_pos = len(sentences) - 1 - (number_of_sentences_around * 2) - 1
            max_pos = len(sentences) - 1
        else:
            # surrounding sentences
            min_pos = index_with_top_match - number_of_sentences_around
            max_pos = index_with_top_match + number_of_sentences_around

        for sentence_index in range(min_pos, max_pos + 1):

            sentence = sentences[sentence_index]
            offset = len(text_full)
            sentence_text_adjusted = adjust_punctuation(sentence['text'])
            text_full += sentence_text_adjusted + " "

            # finding positions for claims
            if SEARCH_KEY_CLAIM in where_to_search:
                sentence.setdefault("claims", [])
                for claim in sentence["claims"]:
                    if float(claim["score"]) > float(confidence) / 100:
                        claim_adjusted = adjust_punctuation(claim["text"])
                        start_pos = sentence_text_adjusted.find(claim_adjusted)
                        end_pos = start_pos + len(claim_adjusted)
                        arguments_positions.append(
                            {"type": "claim", "start": offset + start_pos, "end": offset + end_pos})

            # finding positions for premises
            if SEARCH_KEY_PREMISE in where_to_search:
                sentence.setdefault("premises", [])
                for premise in sentence["premises"]:
                    if float(premise["score"]) > float(confidence) / 100:
                        premise_adjusted = adjust_punctuation(premise["text"])
                        start_pos = sentence_text_adjusted.find(premise_adjusted)
                        end_pos = start_pos + len(premise_adjusted)
                        arguments_positions.append(
                            {"type": "premise", "start": offset + start_pos, "end": offset + end_pos})

            # finding positions for entities
            if SEARCH_KEY_ENTITY in where_to_search:
                sentence.setdefault("entities", [])
                for entity in sentence["entities"]:
                    if entity["class"].upper() == "ORGANIZATION":
                        type = "ORG"
                    elif entity["class"].upper() == "LOCATION":
                        type = "LOC"
                    else:
                        type = entity["class"]
                    text = adjust_punctuation(entity["text"])
                    start_pos = sentence_text_adjusted.find(text)
                    end_pos = start_pos + len(text)
                    entity_positions.append({
                        "type": type,
                        "start": offset + start_pos,
                        "end": offset + end_pos
                    })

        # finding positions for search query instances
        for word in query_words:
            for match in set(re.findall(word, text_full, re.IGNORECASE)):
                positions = [
                    {"type": "search", "start": m.start(), "end": m.end()}
                    for m in re.finditer(match, text_full)
                ]
                query_search_positions.extend(positions)

        app.logger.debug('Full text: %s', text_full)

        doc["text_full"] = text_full
        doc["query_positions"] = query_search_positions
        doc["arguments_positions"] = arguments_positions
        doc["entity_positions"] = entity_positions
        doc["url"] = hit["_source"]["url"]
        docs.append(doc)

    return json.dumps(docs)


def adjust_punctuation(text):
    return re.sub(r'\s([?.!,:;\'"](?:\s|$))', r'\1', text)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=config["host"], port=int(config["port"]), debug=False)

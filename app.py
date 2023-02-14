import argparse
import os
import traceback
import json 

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, make_response
from flask_compress import Compress

from flask_cors import CORS
import polymath

from polymath import (Library, get_completion_with_context, get_embedding,
                        get_max_tokens_for_completion_model)

DEFAULT_CONTEXT_TOKEN_COUNT = 1500
DEFAULT_TOKEN_COUNT = 1000

app = Flask(__name__)
cors = CORS(app)

Compress(app)

load_dotenv()
openai.api_key = "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"
library_filename = "libraries/sitemap-polymathgpt.000webhostapp.com-sitemap1.xml.json"

library = polymath.load_libraries(library_filename, True)
config = polymath.host_config()


@app.route("/", methods=["POST"])
def index():
    print("The config")
    print(config)
    try:
        query = request.args.get('query')
        query_vector = Library.base64_from_vector(
        get_embedding(query))
        decoded = query_vector.decode("utf-8")
        query_embedding = decoded
        query_embedding_model = Library.EMBEDDINGS_MODEL_ID
        count = request.form.get(
            "count", DEFAULT_TOKEN_COUNT, type=int)
        count_type = request.form.get("count_type")
        version = request.form.get('version', -1, type=int)
        
        
        seed = request.form.get('seed')
        
        access_token = request.form.get('access_token', '')
        print("Query embedding model is")
        #print(type(decoded))
        result = library.query(version=1, query_embedding=query_embedding,
                               query_embedding_model=query_embedding_model, count=count)
        print(result.serializable())

        libra = Library(data=((result.serializable())))
        if libra.message:
            print(f'said: ' + library.message)
        else :
            print("no message")
        print(type(jsonify(result.serializable())))
        return (jsonify(result.serializable()))

    except Exception as e:
        return jsonify({
            "errorah": f"{e}\n{traceback.format_exc()}"
        })


@app.route("/", methods=["GET"])
def render_index():
    return "Server is Online"


if __name__ == "__main__":

    app.run()





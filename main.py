#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko

#
# import vertexai
# from vertexai.language_models import TextGenerationModel
#
# from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file('./key.json')


app = Flask(__name__)
app.debug = True

# vertexai.init(project="gcp-adventure-x", location="us-central1", credentials=credentials)
# parameters = {
#     "temperature": 1,
#     "max_output_tokens": 256,
#     "top_p": 0.8,
#     "top_k": 40
# }
#
# model = TextGenerationModel.from_pretrained("text-bison@001")
#

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("chat.html")


@app.route('/pico', methods=['GET'])
def pico_page():
    return render_template("pico.html")

# @app.route('/chat/<message>', methods=['GET'])
# def chat(message):
#     response = model.predict(
#         "generate a poem with the message that follows, make it sound like shakespeare, make it funny, no longer than 12 lines: " + message,
#         **parameters
#     )
#
#     print(response)
#
#     return jsonify({
#         "response": marko.convert(response.text)
#     })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
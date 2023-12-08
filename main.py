#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko
import vertexai
from vertexai.language_models import TextGenerationModel

app = Flask(__name__)
app.debug = True

vertexai.init(project="gcp-adventure-x", location="us-central1")
parameters = {
    "temperature": 1,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

model = TextGenerationModel.from_pretrained("text-bison@001")


@app.route('/', methods=['GET'])
def hello_world():
    return render_template("chat.html")


@app.route('/pico', methods=['GET'])
def pico_page():
    return render_template("pico.html")

@app.route('/chat/<guess>/<actual>', methods=['GET'])
def chat(guess, actual):
    response = model.predict(
        "You are a bot in a guessing game where the player tries to guess a secret item you are thinking about. The player has just guessed " + guess + ". If the user is right, tell them they are right and ask them to refresh the page to start a new game. If they are not very close to the actual item, respond with a humorous remark about their guess, related somehow to their guess and the actual secret item, which is " + actual + ". Then provide a subtle hint to guide the player closer to the actual secret item. Never in your response include the actual item name unless the user has guessed it correctly is is very very close!",
        **parameters
    )

    return jsonify({
        "response": marko.convert(response.text)
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
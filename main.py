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

@app.route('/chat/<guess>/<actual>', methods=['GET'])
def chat(guess, actual):
    response = model.predict(
        "You are the bot in a guessing game where the player tries to guess a secret item you are thinking about. " +
        "The rules of the game are: 1. the player will make a guess. 2. if the guess is correct or very close to the correct answer, you will say, 'Congratulations, you've got it right!' " +
         "3. If they are not very close to the actual item, respond with a humorous remark about their guess. Then without mentioning the actual item, " + actual + ", provide a subtle hint to guide the player closer to the secret item." +
        "The player has just guessed " + guess + ".",
        **parameters
    )

    return jsonify({
        "response": marko.convert(response.text)
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
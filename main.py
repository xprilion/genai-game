#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
app.debug = True


defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.25,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0,
}


@app.route('/', methods=['GET'])
def hello_world():
    return render_template("chat.html")

@app.route('/chat/<guess>/<actual>', methods=['GET'])
def chat(guess, actual):

    context = "You are the bot in a guessing game where the player tries to guess a secret item you are thinking about. " + \
        "The rules of the game are: " + \
        "1. the player will make a guess. " + \
        "2. if the guess is correct or very close to the correct answer, you will say, 'Congratulations, you've got it right!' " + \
        "3. If they are not very close to the actual item, respond with a humorous remark about their guess. Then without mentioning the actual item, " + actual + ", provide exactly one hint to guide the player closer to the secret item. Don't repeat player's input. Don't give many hints at once."
    
    examples = [
        [
            "actual_item: cat. player_input: is it green",
            "They are mostly never green but are often found in black, white and mixed colors."
        ],
        [
            "actual_item: cat. player_input: a car?",
            "Instead of four wheels it has four legs!"
        ],
        [
            "actual_item: cat. player_input: a dog?",
            "You're very close! Yes it is a pet, but not a dog!"
        ],
        [
            "actual_item: cat. player_input: is it a cat?",
            "Congratulations, yes it is a cat!"
        ]
    ]

    prompt = "actual_input: " + actual + ". player_input: " + guess

    response = genai.chat(
        **defaults,
        context=context,
          examples=examples,
        messages=[prompt]
    )

    return jsonify({
        "response": marko.convert(response.last)
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
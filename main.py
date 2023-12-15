#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, request, Response, g, render_template, jsonify
import marko
import google.generativeai as genai
import json

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
app.debug = True


config = {
  'temperature': 0,
  'top_k': 20,
  'top_p': 0.9,
  'max_output_tokens': 500
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=config,
                              safety_settings=safety_settings)

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

    response = model.generate_content(context + "\n\nExamples: " + json.dumps(examples) + "\n\n" + prompt)

    return jsonify({
        "response": marko.convert(response.text)
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
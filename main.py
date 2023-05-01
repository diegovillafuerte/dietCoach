import os
import openai
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Replace 'your_openai_api_key' with your actual OpenAI API key
openai.api_key = "your_openai_api_key"

def get_calories(food_description):
    prompt = f"How many calories are in {food_description}?"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        food_description = request.form["food_description"]
        calories = get_calories(food_description)

        # Save the result to a file or database
        with open("food_calories.txt", "a") as f:
            f.write(f"{food_description}: {calories}\n")

        return render_template("index.html", food_description=food_description, calories=calories)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, make_response
from .user_input import get_calories

app = Flask(__name__)

@app.after_request
def add_vary_cookie_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        food_description = request.form["food_description"]
        calories = get_calories(api_key, food_description)

        return render_template("index.html", food_description=food_description, calories=calories)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

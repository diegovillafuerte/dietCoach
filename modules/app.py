import os
import sys
from flask import Flask, request, render_template, redirect, session, g
from .prompts import get_nutritional_info
from datetime import datetime
from .dbOperations import create_connection, close_connection, add_meal, get_daily_meal_summary
import json
from .dbOperations import DBSession, User, Meal
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET"])
def index():
    if 'username' not in session:
        return redirect('/login')
    return redirect('/welcome')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session = DBSession()
        user = session.query(User).filter_by(email=email).first()        
        if user and pbkdf2_sha256.verify(password, user.password_hash):
            session['email'] = email
            return redirect('/welcome')
        else:
            return render_template('login.html', error="Invalid E-Mail or password")
    else:
        return render_template('login.html')

@app.route("/welcome", methods=["GET", "POST"])
def welcome_route():
    if request.method == "POST":
        food_description = request.form["food_description"]
        nut_info= get_nutritional_info(food_description)
        try:
            nutritional_info = json.loads(nut_info)
        except json.JSONDecodeError:
            return render_template('welcome.html', error="Error: Your query was not understood. Please try again.")
        calories = nutritional_info['calories']
        carbohydrates = nutritional_info['carbohydrates']
        protein = nutritional_info['protein']
        fat = nutritional_info['fat']
        sodium = nutritional_info['sodium']

        # Add the new meal to the database
        current_date = datetime.now().strftime("%Y-%m-%d")
        meal = {
            'meal': food_description,
            'calories': calories,
            'carbohydrates': carbohydrates,  # Replace with actual value
            'protein': protein,        # Replace with actual value
            'fat': fat,            # Replace with actual value
            'sodium': sodium,         # Replace with actual value
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_email': session['email']
        }
        add_meal(g.conn, meal)

        # Get the sum of all meal attributes for the current day
        meals_sum = get_daily_meal_summary(g.conn, current_date, session['email'])
        daily_summary = f"Total calories: {meals_sum[0]}, Total carbohydrates: {meals_sum[1]}, Total protein: {meals_sum[2]}, Total fat: {meals_sum[3]}, Total sodium: {meals_sum[4]}"
        return render_template('welcome.html', daily_summary=daily_summary)
    else:
        return render_template('welcome.html', daily_summary="")
    
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect('/login')

@app.after_request
def add_vary_cookie_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    sys.exit("Error: OPENAI_API_KEY environment variable not set.")

@app.before_request
def before_request():
    g.conn = create_connection()

@app.teardown_request
def teardown_request(exception):
    close_connection(g.conn)

if __name__ == "__main__":
    app.run(debug=True)
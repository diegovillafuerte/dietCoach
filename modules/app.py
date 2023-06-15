import os
import sys
from flask import Flask, request, render_template, redirect, session, g, flash
from .prompts import get_nutritional_info
from datetime import datetime
from .dbOperations import create_connection, close_connection, add_meals, get_daily_total, todays_meals, delete_meals
from .dbOperations import DBSession, User, Meal
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET"])
def index():
    if 'email' not in session:
        return redirect('/login')
    return redirect('/welcome')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db_Session = DBSession()
        user = db_Session.query(User).filter_by(email=email).first()        
        if user and pbkdf2_sha256.verify(password, user.password_hash):
            session['email'] = email
            return redirect('/welcome')
        else:
            return render_template('login.html', error="Invalid E-Mail or password")
    else:
        return render_template('login.html')
    
@app.route("/welcome", methods=["GET"])
def welcome():
    if 'email' not in session:
        return redirect('/login')
    else:
        user_email = session['email']
        todaysMeals = todays_meals(g.conn, user_email)
        dailyTotal = get_daily_total(g.conn, user_email)       
        return render_template('welcome.html', email=user_email, today_meals = todaysMeals, dailyTotal=dailyTotal)

@app.route("/get_info", methods=["POST"])
def get_info():
    food_description = request.form["food_description"]
    nutritional_info = get_nutritional_info(food_description)
    user_email = session['email']
    todaysMeals = todays_meals(g.conn, user_email)
    dailyTotal = get_daily_total(g.conn, user_email) 
    if nutritional_info['calories'] == 'error':
        flash("Error: Your query was not understood. Please try again.")
        return render_template('welcome.html', today_meals = todaysMeals, dailyTotal=dailyTotal, error="Error: Your query was not understood. Please try again.")
        
    # Store the food description and nutritional info in session
    session['food_description'] = food_description
    session['nutritional_info'] = nutritional_info

    return render_template('welcome.html',email=session['email'], nutritional_info=nutritional_info, food_description=food_description, today_meals = todaysMeals, dailyTotal=dailyTotal)


@app.route("/add_meal", methods=["POST"])
def add_meal():
    # Retrieve the food description and nutritional info from session
    food_description = session.get('food_description')
    nutritional_info = session.get('nutritional_info')

    # If the food description or nutritional info are not found in session, redirect to welcome page
    if not food_description or not nutritional_info:
        return redirect('/welcome')

    # Add the new meal to the database
    current_date = datetime.now().strftime("%Y-%m-%d")
    meal = {
        'meal': food_description,
        'calories': nutritional_info['calories'],
        'carbohydrates': nutritional_info['carbohydrates'],
        'protein': nutritional_info['protein'],
        'fat': nutritional_info['fat'],
        'sodium': nutritional_info['sodium'],
        'explanation': nutritional_info['explanation'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'user_email': session['email']
    }
    add_meals(g.conn, meal)

    # Clear the food description and nutritional info from session
    session.pop('food_description', None)
    session.pop('nutritional_info', None)

    # Get todays meal summary
    user_email = session['email']
    todaysMeals = todays_meals(g.conn, user_email)
    dailyTotal = get_daily_total(g.conn, user_email) 

    # Redirect to welcome page
    return render_template('welcome.html', today_meals = todaysMeals, dailyTotal=dailyTotal)

@app.route("/deleteMeal/<int:meal_id>", methods=["GET"])
def delete_Meal(meal_id):
    """
    Deletes the meal with the specified ID from the database.

    Args:
        meal_id: ID of the meal to delete.

    Returns:
        A redirect to the home page.
    """
    try:
        delete_meals(g.conn, meal_id)
    except ValueError as e:
        print(e) 
    user_email = session['email']
    todaysMeals = todays_meals(g.conn, user_email)
    dailyTotal = get_daily_total(g.conn, user_email)       
    return render_template('welcome.html', email=user_email, today_meals = todaysMeals, dailyTotal=dailyTotal)

    
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
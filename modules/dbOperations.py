import os
import psycopg2

def create_connection():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

def close_connection(conn):
    conn.close()

def create_meal_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS meals (
                        id SERIAL PRIMARY KEY,
                        meal TEXT NOT NULL,
                        calories INTEGER NOT NULL,
                        carbohydrates INTEGER,
                        protein INTEGER,
                        fat INTEGER,
                        sodium INTEGER,
                        date TIMESTAMP NOT NULL)''')
    conn.commit()

def add_meal(conn, meal):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO meals (meal, calories, carbohydrates, protein, fat, sodium, date) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''', (meal['meal'], meal['calories'], meal['carbohydrates'], meal['protein'], meal['fat'], meal['sodium'], meal['date']))
    meal_id = cursor.fetchone()[0]
    conn.commit()
    return meal_id

def update_meal(conn, meal):
    cursor = conn.cursor()
    cursor.execute('''UPDATE meals SET meal = %s, calories = %s, carbohydrates = %s, protein = %s, fat = %s, sodium = %s, date = %s WHERE id = %s''', (meal['meal'], meal['calories'], meal['carbohydrates'], meal['protein'], meal['fat'], meal['sodium'], meal['date'], meal['id']))
    conn.commit()

def get_meals(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM meals''')
    return cursor.fetchall()

def get_meal(conn, meal_id):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM meals WHERE id = %s''', (meal_id,))
    return cursor.fetchone()

def get_daily_meal_summary(conn, date_str):
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(calories) as total_calories,
                             SUM(carbohydrates) as total_carbohydrates,
                             SUM(protein) as total_protein,
                             SUM(fat) as total_fat,
                             SUM(sodium) as total_sodium
                      FROM meals
                      WHERE date("date") = %s''', (date_str,))

    return cursor.fetchone()


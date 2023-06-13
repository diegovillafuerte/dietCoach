import sqlite3


conn = sqlite3.connect('calorie_tracker.db')
cursor = conn.cursor()
cursor.execute('''SELECT * FROM meals''')
print(cursor.fetchall())
conn.close()



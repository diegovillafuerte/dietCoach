from dbOperations import Base, User, create_connection, add_meals
from datetime import date


dbsession = create_connection()

user = {
    'email': 'diego.villafuerte.soraiz@gmail.com',
    'name': 'Diego Villafuerte Soraiz',
    'password': '12345678',
    'birthdate': '1993-10-05 00:00:00',
    'weight': 83,
    'height': 170,
    'weight_goal': 68,
    'gender': 'male'
}


'''new_user = add_user(dbsession, user)
print(f"Added user with email: {new_user}")'''

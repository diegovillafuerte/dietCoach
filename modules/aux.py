from dbOperations import Base, User, create_connection, add_user, todays_meals
from datetime import date


dbsession = create_connection()


user1 = {
    'email': 'diego.villafuerte.soraiz@gmail.com',
    'name': 'Diego Villafuerte Soraiz',
    'password': '1234',
    'birthdate': '1993-05-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

user2 = {
    'email': 'bearamirez24@gmail.com',
    'name': 'Beatriz Ramirez',
    'password': '1234',
    'birthdate': '1993-05-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'female'
}

user3 = {
    'email': 'jsilvala@chicagobooth.edu',
    'name': 'Juan Carlos Silva',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

user4 = {
    'email': 'clehuede@mba2024.hbs.edu',
    'name': 'Cristian Lehuede',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

user5 = {
    'email': 'aleblanc@mba2024.hbs.edu',
    'name': 'Antonio Le Blanc',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

user6 = {
    'email': 'jp1080@msn.com',
    'name': 'Juan Pablo Villafuerte',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

user7 = {
    'email': 'camilarm@mit.edu',
    'name': 'Camila Rioseco',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}

add_user(dbsession, user7)
'''
add_user(dbsession, user2)
new_user = add_user(dbsession, user3)
print(f"Added user with email: {new_user}")'''

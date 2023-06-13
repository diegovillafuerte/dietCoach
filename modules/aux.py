from dbOperations import Base, User, create_connection, add_user, remove_user

session = create_connection()

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

new_user = add_user(session, user)

print(f"Added user with email: {new_user}")
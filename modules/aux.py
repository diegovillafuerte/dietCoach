from dbOperations import Base, User, create_connection, add_user
from datetime import date


dbsession = create_connection()

user = {
    'email': 'jsilvala@chicagobooth.edu',
    'name': 'Juan Carlos Silva',
    'password': '12345678',
    'birthdate': '1994-10-10 00:00:00',
    'weight': 65,
    'height': 170,
    'weight_goal': 61,
    'gender': 'male'
}


new_user = add_user(dbsession, user)
print(f"Added user with email: {new_user}")

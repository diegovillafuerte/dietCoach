dietCoach
Overview
dietCoach is a Python-based web application that allows users to log meals and receive nutritional information. It leverages the Flask web development framework and connects with a database to store meal data.

Technology Stack
Python
Flask
Database for storing meal data (specific database technology not specified)
OpenAI API
Application Structure
The application's core functionality is located within the modules directory, which contains several Python files.

Key Files
app.py
The app.py file is the entry point of the application, and it is where the Flask app is initialized and routes are defined. It includes routes for login, logout, and a welcome page. The welcome page is where users can enter a description of a food item, which is then processed to extract nutritional information. This information is stored in a database.

The app uses the pbkdf2_sha256 method from passlib.hash to verify user passwords, indicating that it's storing hashed passwords rather than plain text ones for security reasons.

A session mechanism is used to handle user login state. The session data is tied to a user's email.

dbOperations.py
The dbOperations module handles database operations, including functions for creating and closing database connections, as well as adding meals and getting daily meal summaries.

Installation and Usage
Please follow these steps to install and use the app:

Clone the repository to your local machine.
Install the required dependencies using pip install -r requirements.txt.
Set up the database using the instructions provided in dbSetup.md.
Run the app using python app.py.
Navigate to http://localhost:5000 in your web browser to use the app.
Contributing
Please see CONTRIBUTING.md for information on how to contribute to this project.

License
This project is licensed under the MIT License. See LICENSE for more information.


class User:
    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    def __str__(self):
        return f"User: {self.firstName} {self.lastName} - Email: {self.email}"

class Meal:
    calories = 0
    carbohydrates = 0
    protein = 0
    fat = 0
    sodium = 0
    def __init__(self, description):
        self.description = description
    def __str__(self):
        return f"{self.description}"

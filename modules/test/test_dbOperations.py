import unittest
from dbOperations import remove_user, add_user, add_meals, delete_meals, list_of_days_meals, get_daily_total, get_user
import datetime

class TestDBOperations(unittest.TestCase):
    def test_add_user(self):
        user = {
            'email': 'test@example.com',
            'name': 'Test User',
            'birthdate': datetime.date(1990, 1, 1),
            'weight': 150,
            'height': 70,
            'weight_goal': 140,
            'gender': 'M',
            'password': 'password'
        }
        result = add_user(user)
        self.assertEqual(result, 'test@example.com')

    def test_remove_user(self):
        email = 'test@example.com'
        result = remove_user(email)
        self.assertTrue(result)

    def test_add_meals(self):
        meal = {
            'meal': 'Spaghetti and Meatballs',
            'calories': 800,
            'carbohydrates': 100,
            'protein': 40,
            'fat': 30,
            'sodium': 1000,
            'date': '2022-01-01',
            'explanation': 'A classic Italian dish',
            'user_email': 'test@example.com'
        }
        result = add_meals(meal)
        self.assertIsInstance(result, int)

    def test_delete_meals(self):
        meal_id = 1
        with self.assertRaises(ValueError):
            delete_meals(meal_id)
        
    def test_list_of_days_meals(self):
        user_email = 'test@example.com'
        day = datetime.date(2022, 1, 1)
        result = list_of_days_meals(user_email, day)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_daily_total(self):
        user_email = 'test@example.com'
        day = datetime.date(2022, 1, 1)
        result = get_daily_total(user_email, day)
        self.assertIsInstance(result, dict)
        self.assertGreater(result['calories'], 0)
        self.assertGreater(result['carbohydrates'], 0)
        self.assertGreater(result['protein'], 0)
        self.assertGreater(result['fat'], 0)
        self.assertGreater(result['sodium'], 0)
    
    def test_get_user(self):
        email = 'test@example.com'
        result = get_user(email)
        self.assertIsNotNone(result)
        self.assertEqual(result.email, email)

    def test_get_nonexistent_user(self):
        email = 'nonexistent@example.com'
        result = get_user(email)
        self.assertIsNone(result)
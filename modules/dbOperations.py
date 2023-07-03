from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
from passlib.hash import pbkdf2_sha256
from datetime import date, timedelta

# Manage Database Connection
DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

# Meal class and related methods

class Meal(Base):
    """
    A class representing a meal in the database.

    Attributes:
        id (int): The unique ID of the meal.
        meal (str): The name of the meal.
        calories (int): The number of calories in the meal.
        carbohydrates (int): The number of carbohydrates in the meal.
        protein (int): The number of protein in the meal.
        fat (int): The number of fat in the meal.
        sodium (int): The amount of sodium in the meal.
        date (datetime): The date and time the meal was consumed.
        explanation (str): An optional explanation or note about the meal.
        user_email (str): The email address of the user who added the meal.
        user (User): The user who added the meal.

    Methods:
        __repr__(): Returns a string representation of the meal.
    """
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    carbohydrates = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    sodium = Column(Integer)
    date = Column(DateTime, nullable=False)
    explanation = Column(String)
    user_email = Column(String, ForeignKey('users.email'))
    user = relationship('User', back_populates="meals")

    def __repr__(self):
        return [self.id, self.meal, self.calories, self.carbohydrates, self.protein, self.fat, self.sodium, self.date, self.user_email]

def add_meals(meal):
    """
    Adds a new meal to the database.

    Args:
        DBSession: A SQLAlchemy session object.
        meal: A dictionary containing the meal data.

    Returns:
        The ID of the newly added meal.
    """
    # Create a new Meal object with the data from the meal dictionary.
    new_meal = Meal(
        meal=meal['meal'],
        calories=meal['calories'],
        carbohydrates=meal['carbohydrates'],
        protein=meal['protein'],
        fat=meal['fat'],
        sodium=meal['sodium'],
        date=meal['date'],
        explanation=meal['explanation'],
        user_email=meal['user_email']
    )

    # Create a new session, add the new meal to the database session and commit the transaction.
    with DBSession() as session:
        session.add(new_meal)
        session.commit()



def delete_meals(meal_id):
    """
    Deletes the meal with the specified ID from the database.

    Args:
        meal_id: ID of the meal to delete.

    Returns:
        None.
    """
    with DBSession() as session:
        meal = session.query(Meal).filter(Meal.id == meal_id).first()
        if meal:
            session.delete(meal)
            session.commit()
        else:
            raise ValueError(f"No meal found with ID {meal_id}")

def list_of_days_meals(user_email, day):
    """
    Returns a list of meals for the specified user on the specified day.

    Args:
        DBSession: A SQLAlchemy session object.
        user_email (str): The email address of the user.
        day (datetime.date): The date to retrieve meals for.

    Returns:
        A list of dictionaries representing the meals for the specified user on the specified day.
    """
    with DBSession() as session:
        meals = session.query(Meal).filter(
            Meal.user_email == user_email,
            func.date(Meal.date) == day
        ).all()
        meal_list = []
        for meal in meals:
            meal_dict = {
                'id': meal.id,
                'meal': meal.meal,
                'calories': meal.calories,
                'carbohydrates': meal.carbohydrates,
                'protein': meal.protein,
                'fat': meal.fat,
                'sodium': meal.sodium,
                'date': meal.date,
                'user_email': meal.user_email,
                'explanation': meal.explanation
            }
            meal_list.append(meal_dict)
    return meal_list

def get_daily_total(user_email, day):
    """
    Returns the total nutritional values for all meals for the specified date and user.

    Args:
        DBSession: A SQLAlchemy session object.
        user_email (str): The email address of the user.
        day (datetime.date): The date to retrieve meals for.

    Returns:
        A dictionary containing the total nutritional values for all meals for the specified date and user.
        The dictionary contains the following keys:
            - 'calories': The total number of calories.
            - 'carbohydrates': The total number of carbohydrates.
            - 'protein': The total amount of protein.
            - 'fat': The total amount of fat.
            - 'sodium': The total amount of sodium.
    """
    with DBSession() as session:
        result = session.query(
            func.sum(Meal.calories).label('total_calories'),
            func.sum(Meal.carbohydrates).label('total_carbohydrates'),
            func.sum(Meal.protein).label('total_protein'),
            func.sum(Meal.fat).label('total_fat'),
            func.sum(Meal.sodium).label('total_sodium')
        ).filter(func.date(Meal.date) == day, Meal.user_email == user_email).first()
        total_dic = {
                'calories': result.total_calories,
                'carbohydrates': result.total_carbohydrates,
                'protein': result.total_protein,
                'fat': result.total_fat,
                'sodium': result.total_sodium,
            }
    return total_dic

def get_meals_and_totals_last_Ndays(user_email, time_period):
    """
    Returns a dictionary containing the total nutritional values and a list of meals for the specified user for the last three months.

    Args:
        DBSession: A SQLAlchemy session object.
        user_email (str): The email address of the user.

    Returns:
        A dictionary where each key is a date from the last three months and each value is a dictionary containing:
            - 'totals': A dictionary of the total nutritional values for all meals for the specified date and user.
            - 'meals': A list of dictionaries representing the meals for the specified user on the specified date.
    """
    meals_and_totals = []

    for i in range(time_period-1, -1, -1): 
        day = date.today() - timedelta(days=i)
        day_string = day.isoformat()

        daily_totals = get_daily_total(user_email, day)
        meals = list_of_days_meals(user_email, day)

        meals_and_totals.append((day_string, {
            'totals': daily_totals,
            'meals': meals
        }))

    return meals_and_totals


class User(Base):
    """
    A class representing a user in the database.

    Attributes:
        email (str): The email address of the user (primary key).
        password_hash (str): The hashed password of the user.
        name (str): The name of the user.
        birthdate (datetime): The birthdate of the user.
        weight (int): The weight of the user in pounds.
        height (int): The height of the user in inches.
        weight_goal (int): The weight goal of the user in pounds.
        gender (str): The gender of the user ('M' or 'F').
        meals (list): A list of meals associated with the user.

    Methods:
        __repr__(): Returns a string representation of the user.
        set_password(password): Sets the password hash for the user.
        check_password(password): Checks if the provided password matches the user's password hash.
    """
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    birthdate = Column(DateTime)
    weight = Column(Integer)
    height = Column(Integer)
    weight_goal = Column(Integer)
    gender = Column(String)
    meals = relationship("Meal", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', birthdate={self.birthdate}, email='{self.email}', weight={self.weight}, height={self.height}, weight_goal={self.weight_goal}, gender='{self.gender}'>"
    
    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
    
def get_user(email):
    """
    Retrieves a user from the database by email address.

    Args:
        DBSession: A SQLAlchemy session object.
        email (str): The email address of the user to retrieve.

    Returns:
        A User object representing the user with the specified email address, or None if no such user exists.
    """
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except:
        return None
    finally:
        session.close()

def add_user(email, password, name):
    """
    Adds a new user to the database.

    Args:
        user (dict): A dictionary containing the user's information.
            The dictionary must contain the following keys:
                - 'email': The email address of the user (required).
                - 'name': The name of the user (required).

    Returns:
        The email address of the newly created user.
    """
    new_user = User(
        email=email,
        name=name
    )
    new_user.set_password(password)
    with DBSession() as session:
        session.add(new_user)
        session.commit()
        email_x = new_user.email
    return email_x

def remove_user(email):
    """
    Removes a user from the database by email address.

    Args:
        email (str): The email address of the user to remove.

    Returns:
        True if the user was successfully removed, False otherwise.
    """
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        print("Failed to delete user: ", str(e))
        return False
    finally:
        session.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
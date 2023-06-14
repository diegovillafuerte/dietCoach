from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
from passlib.hash import pbkdf2_sha256
from datetime import date


DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

def create_connection():
    return DBSession()

def close_connection(DBSession):
    DBSession.close()

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    meal = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    carbohydrates = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    sodium = Column(Integer)
    date = Column(DateTime, nullable=False)
    user_email = Column(String, ForeignKey('users.email'))
    user = relationship('User', back_populates="meals")

    def __repr__(self):
        return [self.id, self.meal, self.calories, self.carbohydrates, self.protein, self.fat, self.sodium, self.date, self.user_email]


def add_meals(DBSession, meal):
    new_meal = Meal(
        meal=meal['meal'],
        calories=meal['calories'],
        carbohydrates=meal['carbohydrates'],
        protein=meal['protein'],
        fat=meal['fat'],
        sodium=meal['sodium'],
        date=meal['date'],
        user_email=meal['user_email']
    )
    DBSession.add(new_meal)
    DBSession.commit()
    return new_meal.id

def delete_meals(DBSession, meal_id):
    """
    Deletes the meal with the specified ID from the database.

    Args:
        DBSession: SQLAlchemy session object.
        meal_id: ID of the meal to delete.

    Returns:
        None.
    """
    meal = DBSession.query(Meal).filter(Meal.id == meal_id).first()
    if meal:
        DBSession.delete(meal)
        DBSession.commit()
    else:
        raise ValueError(f"No meal found with ID {meal_id}")

def todays_meals(DBSession, user_email):
    """
    Returns a list of meals for the current day for the specified user.

    Args:
        DBSession: SQLAlchemy session object.
        user_email: Email of the user.

    Returns:
        A list of dictionaries representing the meals for the current day for the specified user.
    """
    today = date.today()
    meals = DBSession.query(Meal).filter(
        Meal.user_email == user_email,
        func.date(Meal.date) == today
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
            'user_email': meal.user_email
        }
        meal_list.append(meal_dict)
    return meal_list



def get_daily_total(DBSession, user_email):
    """
    Returns the total nutritional values for all meals for the specified date and user.

    Args:
        DBSession: SQLAlchemy session object.
        date_str: Date string in the format 'YYYY-MM-DD'.
        user_email: Email of the user.

    Returns:
        A list of total nutritional values for all meals for the specified date and user.
    """
    today = date.today()
    result = DBSession.query(
        func.sum(Meal.calories).label('total_calories'),
        func.sum(Meal.carbohydrates).label('total_carbohydrates'),
        func.sum(Meal.protein).label('total_protein'),
        func.sum(Meal.fat).label('total_fat'),
        func.sum(Meal.sodium).label('total_sodium')
    ).filter(func.date(Meal.date) == today, Meal.user_email == user_email).first()
    total_dic = {
            'calories': result.total_calories,
            'carbohydrates': result.total_carbohydrates,
            'protein': result.total_protein,
            'fat': result.total_fat,
            'sodium': result.total_sodium,
        }
    return total_dic

class User(Base):
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

def add_user(DBSession, user):
    new_user = User(
        email=user['email'],
        name=user['name'],
        birthdate=user['birthdate'],
        weight=user['weight'],
        height=user['height'],
        weight_goal=user['weight_goal'],
        gender=user['gender']
    )
    new_user.set_password(user['password'])
    DBSession.add(new_user)
    DBSession.commit()
    return new_user.email

def remove_user(DBSession, email):
    user = DBSession.query(User).filter_by(email=email).first()
    if user:
        DBSession.delete(user)
        DBSession.commit()
        return True
    else:
        return False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
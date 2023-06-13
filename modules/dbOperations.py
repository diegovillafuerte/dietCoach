from dbCreation import Meal, engine
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def create_connection():
    return Session()

def close_connection(session):
    session.close()

def add_meal(session, meal):
    new_meal = Meal(
        meal=meal['meal'],
        calories=meal['calories'],
        carbohydrates=meal['carbohydrates'],
        protein=meal['protein'],
        fat=meal['fat'],
        sodium=meal['sodium'],
        date=meal['date']
    )
    session.add(new_meal)
    session.commit()
    return new_meal.id

def update_meal(session, meal):
    session.query(Meal).filter_by(id=meal['id']).update({
        'meal': meal['meal'],
        'calories': meal['calories'],
        'carbohydrates': meal['carbohydrates'],
        'protein': meal['protein'],
        'fat': meal['fat'],
        'sodium': meal['sodium'],
        'date': meal['date']
    })
    session.commit()

def get_meals(session):
    return session.query(Meal).all()

def get_meal(session, meal_id):
    return session.query(Meal).filter_by(id=meal_id).first()

def get_daily_meal_summary(session, date_str):
    result = session.query(
        func.sum(Meal.calories).label('total_calories'),
        func.sum(Meal.carbohydrates).label('total_carbohydrates'),
        func.sum(Meal.protein).label('total_protein'),
        func.sum(Meal.fat).label('total_fat'),
        func.sum(Meal.sodium).label('total_sodium')
    ).filter(func.date(Meal.date) == date_str).first()
    return result

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight_goal = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age}, email='{self.email}', weight={self.weight}, height={self.height}, weight_goal={self.weight_goal}, gender='{self.gender}'>"

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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    def __repr__(self):
        return f"<Meal(id={self.id}, meal='{self.meal}', calories={self.calories}, carbohydrates={self.carbohydrates}, protein={self.protein}, fat={self.fat}, sodium={self.sodium}, date={self.date}, user={self.user})>"

if __name__ == '__main__':
    Base.metadata.create_all(engine)
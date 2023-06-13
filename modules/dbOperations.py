from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
from passlib.hash import pbkdf2_sha256

DATABASE_URL = os.environ['DATABASE_URL']
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
        return f"<Meal(id={self.id}, meal='{self.meal}', calories={self.calories}, carbohydrates={self.carbohydrates}, protein={self.protein}, fat={self.fat}, sodium={self.sodium}, date={self.date}, user_email='{self.user_email})>"


def add_meal(DBSession, meal):
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

def get_daily_meal_summary(DBSession, date_str, user_email):
    result = DBSession.query(
        func.sum(Meal.calories).label('total_calories'),
        func.sum(Meal.carbohydrates).label('total_carbohydrates'),
        func.sum(Meal.protein).label('total_protein'),
        func.sum(Meal.fat).label('total_fat'),
        func.sum(Meal.sodium).label('total_sodium')
    ).filter(func.date(Meal.date) == date_str, Meal.user_email == user_email).first()
    return result

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
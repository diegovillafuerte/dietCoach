from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

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
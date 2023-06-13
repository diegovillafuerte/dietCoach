from sqlalchemy.orm import sessionmaker
from dbCreation import Meal, engine

Session = sessionmaker(bind=engine)

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
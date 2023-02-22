import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas import Base, Menu, Dish, DishStats
import datetime

def create_db():
    engine = create_engine('sqlite:///database.db')
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    my_session = sessionmaker(bind=engine)
    print(Base.metadata.tables.keys())
    print(engine.connect())
    return None

class database_handler():
    def __init__(self):
        self.session = None
        engine = create_engine('sqlite:///database.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def close(self):
        self.session.close()
        return None

    def add_dish(self, name, type, ingredients):
        dish = Dish(name=name, type=type, ingredients=ingredients)
        self.session.add(dish)
        self.session.commit()
        return None

    def add_menu(self, date, meal, notes, dish_id):
        datetime_now = datetime.datetime.now()
        menu = Menu(date=date, meal=meal, notes=notes, dish_id=dish_id, edition=datetime_now)
        self.session.add(menu)
        self.session.commit()
        return None
    
    def get_dish(self, dish_id):
        dish = self.session.query(Dish).filter_by(id=dish_id).first()
        return dish

    def get_menu(self, date, meal):
        menu = self.session.query(Menu).filter_by(date=date, meal=meal).first()
        return menu
    
    def query_dishes(self, input): #Where input will be the search string
        dishes = self.session.query(Dish).filter(Dish.name.like('%'+input+'%')).all()
        return dishes

    def query_next_dish_in_menu(self, meal):
        date = datetime.datetime.now().date()
        menu = self.session.query(Menu).filter(Menu.date >= date, Menu.meal >= meal).first()
        return menu

    #stats

    def add_dish_stats(self, dish_id, likes, dislikes, neutrals):
        date = datetime.datetime.now().date()
        dish_stats = DishStats(dish_id=dish_id, date=date, likes=likes, dislikes=dislikes, neutrals=neutrals)
        self.session.add(dish_stats)
        self.session.commit()
        return None
    
    def get_dish_stats(self, dish_id):
        dish_stats = self.session.query(DishStats).filter_by(dish_id=dish_id).all()
        return dish_stats

    def most_liked_dish(self):
        dish_stats = self.session.query(DishStats).order_by(DishStats.likes.desc()).first()
        return dish_stats

    def most_disliked_dish(self):
        dish_stats = self.session.query(DishStats).order_by(DishStats.dislikes.desc()).first()
        return dish_stats


# Example usage:
create_db()
db = database_handler()
db.add_dish("Pasta", "main", "pasta, tomato sauce")
db.add_menu("2019-01-01", 1, "vegetarian", 1)
db.add_dish_stats(1, 3, 0, 0)

print(db.get_dish(1).name)
print(db.get_menu("2019-01-01", 1).notes)
print(db.query_dishes("Pasta")[0].name)
# get last day stats for dish 1
print(db.get_dish_stats(1)[-1].likes)




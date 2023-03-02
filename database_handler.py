import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas import Base, Menu, Dish, DishStats, FeedBack
import datetime


def create_db():
    engine = create_engine('sqlite:///database.db')
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    my_session = sessionmaker(bind=engine)
    print(Base.metadata.tables.keys())
    print(engine.connect())
    return None


class DatabaseHandler():
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
        dish_id = self.get_dish_id(name)
        dish_stats = DishStats(dish_id=dish_id, date=datetime.datetime.now(
        ).date(), likes=0, dislikes=0, neutrals=0)
        self.session.add(dish_stats)
        self.session.commit()
        return None

    def add_menu(self, date, meal, notes, dish_id):
        datetime_now = datetime.datetime.now()
        menu = Menu(date=date, meal=meal, notes=notes,
                    dish_id=dish_id, edition=datetime_now)
        self.session.add(menu)
        self.session.commit()
        return None

    def get_dish(self, dish_id):
        dish = self.session.query(Dish).filter_by(id=dish_id).first()
        return dish

    def get_menu(self, date, meal):
        menu = self.session.query(Menu).filter_by(date=date, meal=meal).first()
        return menu

    def query_dishes(self, input):  # Where input will be the search string
        dishes = self.session.query(Dish).filter(
            Dish.name.like('%'+input+'%')).all()
        return dishes

    def query_next_dish_in_menu(self, meal):
        date = datetime.datetime.now().date()
        menu = self.session.query(Menu).filter(
            Menu.date >= date, Menu.meal >= meal).first()
        return menu

    # stats

    def get_dish_id(self, dish_name):
        dish = self.session.query(Dish).filter_by(name=dish_name).first()
        if dish is None:
            return None
        return dish.id

    def change_dish_stats(self, dish_id, like:int, dislike:int, neutral:int):
        dish_stats = self.session.query(DishStats).filter_by(
            dish_id=dish_id).first()
        dish_stats.likes += like
        dish_stats.dislikes += dislike
        dish_stats.neutrals += neutral
        self.session.commit()
        return None

    def get_all_dish_stats(self): #show the most recent dish stats first
        dish_stats = self.session.query(DishStats).order_by(DishStats.date.desc()).all()
        return dish_stats

    def get_dish_stats(self, dish_id):
        dish_stats = self.session.query(
            DishStats).filter_by(dish_id=dish_id).all()
        return dish_stats

    def most_liked_dish(self):
        dish_stats = self.session.query(DishStats).order_by(
            DishStats.likes.desc()).first()
        return dish_stats

    def most_disliked_dish(self):
        dish_stats = self.session.query(DishStats).order_by(
            DishStats.dislikes.desc()).first()
        return dish_stats
    
    def reset_dish_stats(self, dish_id):
        dish_stats = self.session.query(DishStats).filter_by(
            dish_id=dish_id).first()
        dish_stats.likes = 0
        dish_stats.dislikes = 0
        dish_stats.neutrals = 0
        self.session.commit()
        return None

    # feedback
    def add_feedback(self, feedback_title, dish_id, feedback):
        date = datetime.datetime.now().date()
        feedback = FeedBack(feedback_title=feedback_title, dish_id=dish_id, feedback=feedback, date=date, read_status=0)
        self.session.add(feedback)
        self.session.commit()
        return None

    # show the unread feedback first (read_status = 0) and then the read feedback (read_status = 1), also filtered by date
    def get_feedback(self, dish_id):
        feedback = self.session.query(FeedBack).filter_by(
            dish_id=dish_id).order_by(FeedBack.read_status, FeedBack.date).all()
        for f in feedback:
            if f.read_status == 0:
                f.read_status = "Non Read"
            else:
                f.read_status = "Read"
        return feedback

    # show the unread feedback first (read_status = 0) and then the read feedback (read_status = 1), also filtered by date
    def get_all_feedback(self):
        feedback = self.session.query(FeedBack).order_by(
            FeedBack.read_status, FeedBack.date).all()
        for f in feedback:
            if f.read_status == 0:
                f.read_status = "Non Read"
            else:
                f.read_status = "Read"
        return feedback

    def get_feedback_id(self, title):
        feedback = self.session.query(FeedBack).filter_by(
            feedback_title=title).first()
        return feedback.id

    def mark_feedback_as_read(self, feedback_id):
        feedback = self.session.query(FeedBack).filter_by(
            id=feedback_id).first()
        feedback.read_status = 1
        self.session.commit()
        return None
    
    def delete_feedback(self, feedback_id):
        feedback = self.session.query(FeedBack).filter_by(
            id=feedback_id).first()
        self.session.delete(feedback)
        self.session.commit()
        return None

# Hard coded example usage: (add vegetable dish, meat and dessert)
"""
create_db()
db = DatabaseHandler()

# add them to dish stats
db.change_dish_stats(1, 0, 0, 0)


create_db()
db = DatabaseHandler()
db.add_dish('Vegetable', 'vegetable', 'carrot, potato, onion')
db.add_dish('Meat', 'meat', 'beef, pork, chicken')
db.add_dish('Dessert', 'dessert', 'ice cream, cake, chocolate')

db.add_dish("Chicken Curry", "meat", "chicken, curry, rice")
db.add_dish("Creme Brulee", "dessert", "egg, sugar, cream")
db.add_dish("Pasta", "vegetable", "pasta, tomato, cheese")
db.add_dish("Pizza", "meat", "dough, tomato, cheese")
db.add_dish("Salad", "vegetable", "lettuce, tomato, cucumber")
db.add_dish("Steak", "meat", "beef, salt, pepper")
db.add_dish("Sushi", "meat", "rice, fish, seaweed")
"""

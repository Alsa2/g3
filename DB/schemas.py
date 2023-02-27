from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String) #main, side, dessert
    ingredients = Column(String) #list of ingredients
    menu = relationship("Menu", back_populates="dish")
    dish_stats = relationship("DishStats", back_populates="dish")

class DishStats(Base):
    __tablename__ = 'dish_stats'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dish.id'))
    dish = relationship("Dish", back_populates="dish_stats")
    date = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)
    neutrals = Column(String)

class FeedBack(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dish.id'))
    dish = relationship("Dish", back_populates="feedback")
    date = Column(String)
    feedback = Column(String)
    read_status = Column(Integer) #0 - unread, 1 - read
    


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    date = Column(String) #date
    meal = Column(Integer) # 1, 2, 3
    edition = Column(String) #datetime
    notes = Column(String) #additional information (e.g. "vegetarian")
    dish_id = Column(Integer, ForeignKey('dish.id'))
    dish = relationship("Dish", back_populates="menu")

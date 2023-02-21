from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    date = Column(String) #date
    meal = Column(Integer) # 1, 2, 3
    edition = Column(String) #datetime
    notes = Column(String) #additional information (e.g. "vegetarian")
    dish_id = Column(Integer, ForeignKey('dish.id'))
    dish = relationship("Dish", back_populates="menu")

class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String) #main, side, dessert
    ingredients = Column(String) #list of ingredients
    menu = relationship("Menu", back_populates="dish") 
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db():
    engine = create_engine('sqlite:///database.db', echo=False)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    my_session = session()
    print(Base.metadata.tables.keys())
    print(engine.connect())
    return None



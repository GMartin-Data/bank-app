"""
This file contains all the logic devoted to manage the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, Account, Transaction


def create_tables(engine):
    # Will automatically check if the created tables exist.
    Base.metadata.create_all(engine)

def init_db_connection(connection_string):
    # It seems safer to return both even if you will mainly use
    # context managers like `with session:`
    # You will have to close all with `engine.dispose()`.
    engine = create_engine(connection_string, echo=True)
    return engine, Session(engine) 


# # init_db.py ###
# engine = create_engine('sqlite:///bank.db', echo=True)
# Session = scoped_session(sessionmaker(bind=engine))
# Base.metadata.create_all(engine)

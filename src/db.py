"""
This file contains all the logic devoted to initialize the database, and manage connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# init_db.py ###
Base = declarative_base()
engine = create_engine('sqlite:///library.db')
Session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)

"""
This module contains the models used.
The syntax sticks to SQLAlchemy 1.4
It also contains an utility to create the tables based on the model.
Hence, launched as a script, it will create the tables.
"""

from datetime import datetime

from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db import init_db_connection


Base = declarative_base()


# Classes
class Account(Base):
    __tablename__ = "accounts"
    # Fields
    account_id = Column(Integer, primary_key=True)
    balance = Column(Float)
    # Relationships
    # One-to-Many: one account may have many transactions
    transactions = relationship("Transaction", back_populates="account")

    # Methods
    def __init__(self, balance: float = 0):
        """
        - account_id is an integer automatically generated by SQLAlchemy (auto-incremented)
        - the initial balance is obviously set to 0
        """
        self.balance = balance

    def __repr__(self):
        return f"Account(id={self.account_id}, balance={self.balance})"


class Transaction(Base):
    __tablename__ = "transactions"
    # Fields
    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    amount = Column(Float)
    type = Column(String)
    timestamp = Column(DateTime)
    # Relationships
    # Many-to-One: any transaction has only one account
    account = relationship("Account", back_populates="transactions")

    # Methods
    def __init__(self, account_id, amount, type):
        self.account_id = account_id
        self.amount = amount
        self.type = type
        self.timestamp = datetime.now()


def create_tables(engine):
    # Will automatically check if the created tables exist.
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    engine, session = init_db_connection()
    create_tables(engine)

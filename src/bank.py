"""
This file contains the intrisic logic of bank functionalities, including:
- create_account
- deposit
- withdraw
- transfer
- get_balance

This invoves two mandatory classes:
- Account
- Transaction
"""

from datetime import datetime

from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .init_db import Base


# Classes
class Account(Base):
    __tablename__ = "accounts"
    # Fields
    ...
    # Relationships
    # One-to-Many: one account may have many transactions
    pass

class Transaction(Base):
    __tablename__ = "transactions"
    # Fields
    ...
    # Relationships
    # Many-to-One: any transaction has only one account
    pass


# Functions
def create_account():
    pass

def deposit():
    pass

def withdraw():
    pass

def transfer():
    pass

def get_balance():
    pass

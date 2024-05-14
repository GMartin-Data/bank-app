"""
This module contains the models used.
The syntax sticks to SQLAlchemy 2
"""

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    # Fields
    account_id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float]
    # Relationships
    # One-to-many: one account may have many transactions
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="account"
    )

    # Methods
    def __init__(self, balance: float = 0):
        self.balance = balance


class Transaction(Base):
    __tablename__ = "transactions"

    # Fields
    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.account_id"))
    amount: Mapped[float]
    type: Mapped[str] = mapped_column(String(8))
    timestamp: Mapped[datetime]
    # Relationships
    # Many-to-one: any transaction has only one account
    account: Mapped[int] = relationship(
        back_populates="transaction"
    )

    # Methods
    def __init__(self, account_id, amount, type):
        self.account_id = account_id
        self.amount = amount
        self.type = type
        self.timestamp = datetime.now()

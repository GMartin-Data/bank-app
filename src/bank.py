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

from sqlalchemy.orm import Session

from models_legacy import Account
from db import init_db_connection


# Functions
def create_account(session: Session, amount: float = 0.0) -> None:
    new_account = Account(balance=amount)
    with session:
        session.add(new_account)
        session.commit()

def deposit():
    pass

def withdraw():
    pass

def transfer(account_id_from, account_id_to, amount):
    # # Waiting for decorator
    # engine, session = init_db_connection("sqlite:///bank.db")
    # with session:
    pass

def get_balance(session: Session, account_id: int) -> None:
    with session:
        account = (session
                   .query(Account)
                   .filter(Account.account_id == account_id)
                   .one())
        print(f"Account {account.account_id} has a balance of {account.balance}")
    


if __name__ == "__main__":
    engine, session = init_db_connection()
    get_balance(session, 1)
    engine.dispose()

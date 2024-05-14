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

from db import init_db_connection
from models_legacy import Account


# Functions
def create_account(amount: float = 0.0) -> None:
    new_account = Account(balance=amount)
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

def get_balance():
    pass


if __name__ == "__main__":
    engine, session = init_db_connection()
    with session:
        a = Account()
        print("=====> Before db registering", a)
        session.add(a)
        session.commit()
        print("=====> After db registering", a)
    engine.dispose()

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

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models_legacy import Account, Transaction
from db import init_db_connection


# Utility functions
def is_incorrect_amount(amount):
    try:
        float(amount)
    except ValueError:
        print(f"/!\ TRANSACTION CANCELLED: Expected a numerical amount, got {amount}")
        return True
    if amount < 0:
        print(f"/!\ TRANSACTION CANCELLED: Expected a positive amount, got {amount}")
        return True
    return False
    

# Main Functions
def create_account(session: Session, amount: float = 0.0) -> None:
    new_account = Account(balance=amount)
    with session:
        session.add(new_account)
        session.commit()


def deposit(session: Session, account_id: int, amount: float) -> None:
    if is_incorrect_amount(amount):
        return  None
    with session:
        try:
            account = (session
                       .query(Account)
                       .filter(Account.account_id == account_id)
                       .one())
            account.balance += amount
            session.add(account)
            # Register the corresponding transaction
            approved = Transaction(account_id, amount, "deposit")
            session.add(approved)
            get_balance(session, account_id)
            session.commit()
            print(f"==> TRANSACTION {approved.transaction_id} APPROVED!")
        except NoResultFound:
            print(f"/!\ TRANSACTION CANCELLED: There's no account with id {account_id}")


def withdraw():
    pass

def transfer(account_id_from, account_id_to, amount):
    # # Waiting for decorator
    # engine, session = init_db_connection("sqlite:///bank.db")
    # with session:
    pass

def get_balance(session: Session, account_id: int) -> bool:
    with session:
        try:
            account = (session
                       .query(Account)
                       .filter(Account.account_id == account_id)
                       .one())
            print(f"Account {account.account_id} has a balance of {account.balance}")
        except NoResultFound:
            print(f"/!\ TRANSACTION CANCELLED: There's no account with id {account_id}")
    


if __name__ == "__main__":
    engine, session = init_db_connection()
    # create_account(session, amount=0)
    get_balance(session, account_id=2)
    deposit(session, account_id=1, amount=-10)
    deposit(session, account_id=2, amount="BOUH!")
    deposit(session, account_id=3, amount=20)
    deposit(session, account_id=1, amount=100)
    engine.dispose()

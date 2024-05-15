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
from typing import Union

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models_legacy import Account, Transaction
from db import init_db_connection


# Utility functions
def is_incorrect_amount(amount: Union[int, float]) -> bool:
    try:
        float(amount)
    except ValueError:
        print(f"INCORRECT AMOUNT: Expected a numerical amount, got {amount}")
        return True
    if amount < 0:
        print(f"INCORRECT AMOUNT: Expected a positive amount, got {amount}")
        return True
    return False
    

# Main Functions
def create_account(session: Session, amount: float = 0.0) -> str:
    if is_incorrect_amount(amount):
        output = "CANCELLED CREATION: Incorrect amount prompted"
        print(output)
        return output
    new_account = Account(balance=amount)
    with session:
        session.add(new_account)
        session.commit()
        output = f"APPROVED CREATION of account {new_account.account_id} with an initial balance of {new_account.balance}"
        print(output)
        return output


def deposit(session: Session, account_id: int, amount: float) -> str:
    if is_incorrect_amount(amount):
        output =  "CANCELLED DEPOSIT: Incorrect amount prompted"
        print(output)
        return output
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
            session.commit()
            print(f"APPROVED DEPOSIT - REF: {approved.transaction_id}")
            
        except NoResultFound:
            print(f"CANCELLED DEPOSIT: There's no account with id {account_id}")


def withdraw(session: Session, account_id: int, amount: float) -> str:
    if is_incorrect_amount(amount):
        return "CANCELLED WITHDRAWAL: Incorrect amount prompted"
    with session:
        try:
            account = (session
                       .query(Account)
                       .filter(Account.account_id == account_id)
                       .one())
            if account.balance < amount:
                output = f"CANCELLED WITHDRAWAL: Insufficient funds on account {account_id}"
                print(output)
                return output
            else:
                account.balance -= amount
                session.add(account)
                # Register the corresponding transaction
                approved = Transaction(account_id, amount, "withdraw")
                session.add(approved)
                session.commit()
                output = f"APPROVED WITHDRAWAL - REF: {approved.transaction_id}"
                print(output)
                return output

        except NoResultFound:
            output = f"CANCELLED WITHDRAWAL: There's no account with id {account_id}"
            print(output)
            return output


def transfer(session: Session,
             account_from_id: int, account_to_id: int,
             amount: float) -> None:
    if is_incorrect_amount(amount):
        return None
    with session:
        acc_from = (session
                         .query(Account)
                         .filter(Account.account_id == account_from_id)
                         .all())
        if not acc_from:
            print(f"/!\ TRANSACTION CANCELLED: There's no account with id {account_from_id}")
        else:
            acc_from = acc_from[0]
            if acc_from.balance < amount:
                print(f"/!\ TRANSACTION CANCELLED: Insufficient funds on account {account_from_id}")
            else:
                acc_to = (session
                          .query(Account)
                          .filter(Account.account_id == account_from_id)
                          .all())
                if not acc_to:
                    print(f"/!\ TRANSACTION CANCELLED: There's no account with id {account_to_id}")
                else:
                    acc_to = acc_to[0]
                    acc_to.balance += amount
                    session.add(acc_to)
                    # Register the corresponding 2 transactions
                    approved_from = Transaction(account_from_id, amount, "withdraw")
                    approved_to = Transaction(account_to_id, amount, "deposit")
                    session.add_all([approved_from, approved_to])
                    get_balance(session, account_from_id)
                    get_balance(session, account_to_id)
                    session.commit()
                    print(f"==> TRANSACTIONS {approved_from.transaction_id} and {approved_to.transaction_id} APPROVED!")


def get_balance(session: Session, account_id: int) -> str:
    with session:
        try:
            account = (session
                       .query(Account)
                       .filter(Account.account_id == account_id)
                       .one())
            output = f"INFO: Account {account.account_id} has a balance of {account.balance}"
            print(output)
            return output
        except NoResultFound:
            print(f"CANCELLED INFO: There's no account with id {account_id}")
    


if __name__ == "__main__":
    engine, session = init_db_connection()
    create_account(session, -3_000)
    create_account(session, 200)
    deposit(session, 1, -100)
    deposit(session, 1, "BOUH")
    deposit(session, 42, 1_000)
    deposit(session, 1, 400)
    get_balance(session, 8)
    get_balance(session, 1)
    engine.dispose()

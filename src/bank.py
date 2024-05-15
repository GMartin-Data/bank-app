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

from typing import Union

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from models_legacy import Account, Transaction
from db import init_db_connection


# Utility functions
def is_incorrect_amount(amount: Union[int, float]) -> bool:
    """Utility function to manage non numerical or negative amounts prompted."""
    # Non-numerical
    try:
        float(amount)
    except ValueError:
        print(f"INCORRECT AMOUNT: Expected a numerical amount, got {amount}")
        return True
    # Negative
    if amount < 0:
        print(f"INCORRECT AMOUNT: Expected a positive amount, got {amount}")
        return True
    # Finally, normal case
    return False
    

# Main Functions
def create_account(session: Session, amount: float = 0.0) -> str:
    """
    Create a bank account with specifying an inital balance (default is 0.0).
    `account_id` is automatically generated (auto-incrementation) when recording in database.
    Return value is the informative message displayed, in case of approval or cancellation.
    The account is recorded in the database's `accounts` table.
    """
    if is_incorrect_amount(amount):
        output = "CANCELLED CREATION: Incorrect amount prompted"
        print(output)
        return output
    new_account = Account(balance=amount)
    with session:
        session.add(new_account)
        session.commit()
        output = f"APPROVED CREATION of account {new_account.account_id}" + \
            f" with an initial balance of {new_account.balance:.2f}"
        print(output)
        return output


def deposit(session: Session, account_id: int, amount: float) -> str:
    """
    Perform a deposit on an account, with specifying:
    - its account_id,
    - the wanted amount.
    Return value is the informative message displayed, in case of approval or cancellation.
    This deposit is recorded in the database's `transactions` table.
    """
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
            output = f"APPROVED DEPOSIT of {amount:.2f} on account {account_id}" +\
                f" - REF: {approved.transaction_id}"
            print(output)
            return output
            
        except NoResultFound:
            output = f"CANCELLED DEPOSIT: There's no account with id {account_id}"
            print(output)
            return output


def withdraw(session: Session, account_id: int, amount: float) -> str:
    """
    Perform a withdrawal on an account, with specifying:
    - its account_id,
    - the wanted amount.
    Return value is the informative message displayed, in case of approval or cancellation.
    This withdrawal is recorded in the database's `transactions` table.
    """
    if is_incorrect_amount(amount):
        output = "CANCELLED WITHDRAWAL: Incorrect amount prompted"
        print(output)
        return output
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
                output = f"APPROVED WITHDRAWAL of {amount:.2f} on account {account_id} - REF: {approved.transaction_id}"
                print(output)
                return output

        except NoResultFound:
            output = f"CANCELLED WITHDRAWAL: There's no account with id {account_id}"
            print(output)
            return output


def transfer(session: Session, account_from_id: int, account_to_id: int, amount: float) -> str:
    """
    Perform a transfer between two accounts, with specifying:
    - their account_ids,
    - the wanted amount.
    Return value is the informative message displayed, in case of approval or cancellation.
    This transfer is recorded TWICE in the database's `transactions` table:
    - one withdrawal associated with the "from" account (first),
    - one deposit associated with the "to" account (second).
    """
    if is_incorrect_amount(amount):
        output = "CANCELLED TRANSFER: Incorrect amount prompted"
        print(output)
        return output
    with session:
        acc_from = (session
                         .query(Account)
                         .filter(Account.account_id == account_from_id)
                         .all())
        if not acc_from:
            output = f"CANCELLED TRANSFER: There's no account with id {account_from_id}"
            print(output)
            return output
        else:
            acc_from = acc_from[0]
            if acc_from.balance < amount:
                output = f"CANCELLED TRANSFER: Insufficient funds on account {account_from_id}"
                print(output)
                return output
            else:
                acc_to = (session
                          .query(Account)
                          .filter(Account.account_id == account_to_id)
                          .all())
                if not acc_to:
                    output = f"CANCELLED TRANSFER: There's no account with id {account_from_id}"
                    print(output)
                    return output
                else:
                    acc_to = acc_to[0]
                    acc_to.balance += amount
                    session.add(acc_to)
                    # Register the corresponding 2 transactions
                    approved_from = Transaction(account_from_id, amount, "withdraw")
                    approved_to = Transaction(account_to_id, amount, "deposit")
                    session.add_all([approved_from, approved_to])
                    session.commit()
                    output = f"APPROVED TRANSFER of {amount:.2f} from account {account_from_id} to account {account_to_id}" +\
                    f" - REFS: {approved_from.transaction_id} and {approved_to.transaction_id}"
                    print(output)
                    return output


def get_balance(session: Session, account_id: int) -> str:
    """
    Display the current balance of an account,
    with specifying its id.
    Return value is the informative message displayed, in case of approval or cancellation.
    """
    with session:
        try:
            account = (session
                       .query(Account)
                       .filter(Account.account_id == account_id)
                       .one())
            output = f"INFO: Account {account.account_id} has a current balance of {account.balance:.2f}"
            print(output)
            return output
        except NoResultFound:
            print(f"CANCELLED INFO: There's no account with id {account_id}")
    


if __name__ == "__main__":
    engine, session = init_db_connection()
    # create_account(session, -3_000)
    create_account(session, 200)
    # deposit(session, 1, -100)
    # deposit(session, 1, "BOUH")
    # deposit(session, 42, 1_000)
    # deposit(session, 2, 1_000)
    # deposit(session, 1, 400)
    # withdraw(session, 42, -100)
    # withdraw(session, 1, "BOUH")
    # withdraw(session, 42, 1_000)
    # withdraw(session, 1, 300)
    transfer(session, 1, 2, -100)
    transfer(session, 1, 2, "BOUH")
    transfer(session, 42, 1, 100)
    transfer(session, 1, 42, 100)
    transfer(session, 1, 3, 500)
    # get_balance(session, 42)
    # get_balance(session, 1)
    # get_balance(session, 2)
    engine.dispose()

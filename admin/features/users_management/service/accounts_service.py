from typing import Optional
from sqlmodel import Session, select

from ..data import (
    Account,
    AccountRead,
    AccountCreate,
)
from ..data.exceptions import AccountNotFoundException, LicenseNotValidException

from . import license_service, users_service
from ..data.exceptions import UserNotFoundException

def create_account(session: Session, user_id: int, account: AccountCreate) -> Account:
    # todo: validate that the user exists,
    # can't add an account to non existing user (the user id must be wrong)
    user = users_service.get_user(session, user_id)
    if not user:
        raise UserNotFoundException
    a = Account(**account.model_dump(), user_id=user_id)
    session.add(a)
    session.commit()
    session.refresh(a)
    return a


def get_account_from_uuid(session: Session, uuid: str) :
    account = session.exec(select(Account).where(Account.uuid == uuid)).first()
    if not account:
        raise AccountNotFoundException
    return account
    # return AccountRead.model_validate(account)


def get_all_accounts(session: Session, user_id: Optional[int]) -> list[Account]:
    """returns all accounts stored in the DB, or all accounts of a specific user"""
    stmt = select(Account)
    if user_id:
        stmt = select(Account).where(Account.user_id == user_id)

    return list(session.exec(stmt).all())


def delete_accounts(
    session: Session, user_id: Optional[int], accounts_ids: Optional[list[int]]
):
    if accounts_ids:
        for account_id in accounts_ids:
            session.delete(session.get(Account, account_id))
    if user_id:
        for account in get_all_accounts(session, user_id):
            session.delete(account)
    session.commit()


def update_account():
    pass


def validate_account_license(session: Session, account_uuid: str):
    license = license_service.get_account_license(session, account_uuid)
    valid = license_service.validate_license(license)
    if not valid:
        raise LicenseNotValidException
    account = get_account_from_uuid(session, account_uuid)
    return account

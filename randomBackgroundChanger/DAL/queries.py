
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from randomBackgroundChanger.DAL import database


class InvalidToken(Exception):
    pass


def validToken(token, validateDate=True):
    with Session(database.getEngine()) as session:
        selectTokens = select(database.Token).where(
            database.Token.token == token
        )

        if validateDate:
            selectTokens.where(
                datetime.now() < database.Token.expiryDate
            )

        tokens = session.scalars(selectTokens)

        return len(tokens.all()) != 0


def addNewToken(token, validDays=30):
    with Session(database.getEngine()) as session:
        if validToken(token, validateDate=False):
            raise InvalidToken("Token already exists in the database")

        token = database.Token(
            token=token, expiryDate=datetime.now() + timedelta(days=validDays)
        )

        session.add(token)

        session.commit()


def revokeToken(token):
    with Session(database.getEngine()) as session:
        if not validToken(token, validateDate=False):
            raise InvalidToken("Token doesn't exist in the database")

        deleteStmt = delete(database.Token).where(database.Token.token == token)

        session.execute(deleteStmt)
        session.commit()

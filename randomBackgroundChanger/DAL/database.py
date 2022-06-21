
import os

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def getEngine():
    return create_engine(f"sqlite:///{os.getcwd()}/fileHandler.db", echo=True)


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    expiryDate = Column(DateTime)

    def __repr__(self):
        return f"Token(id={self.id})"


def createTables():
    engine = getEngine()
    Base.metadata.create_all(engine)

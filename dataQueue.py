"""
create db file if not exists
create table 
"""
from sqlalchemy import create_engine, Integer, String, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.exc
import json
import logging
from logging.config import dictConfig

file = open('logging_config.ini', "r")
config = json.load(file)
dictConfig(config)

logger = logging.getLogger(__name__)


Base = declarative_base()


class User(Base):
    __tablename__ = "person"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String, unique=True, nullable=True)
    comment = Column('comment', String)


try:
    engine = create_engine('sqlite:///users.db')
    Base.metadata.create_all(bind=engine)
except sqlalchemy.exc.ArgumentError as e:
    logger.error(e)

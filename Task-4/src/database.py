from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # create sqlachemy to poetgres

session = sessionmaker(     # create database session
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()      # parent class for database


def get_db():       # provide database session to fastApi
    db = session()
    try:
        yield db
    finally:
        db.close()
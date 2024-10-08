import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)

Base = declarative_base()

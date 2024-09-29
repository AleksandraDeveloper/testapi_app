# этот файл описывает подключение к БД
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL") #"postgresql+psycopg2://postgres_user:postgres_password@db:5432/superapp_db" #?client_encoding=utf8


engine = create_engine(DATABASE_URL)

# сешионмэйкер нужен для создания сессий
session_local = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)  # аргументы отключают автосинхронизацию с БД и автокомит

Base = declarative_base()
# эта функция на основе моделей создает таблицы в БД

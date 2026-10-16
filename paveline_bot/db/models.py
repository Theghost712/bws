from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)


class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=True)
    relationship = Column(String, default="friend")
    language = Column(String, default="en")
    style = Column(String, default="heartfelt")
    remind = Column(Boolean, default=True)
    remind_days_before = Column(Integer, default=1)
    chat_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class SentLog(Base):
    __tablename__ = "sent_log"

    id = Column(Integer, primary_key=True, index=True)
    birthday_id = Column(Integer, index=True)
    sent_date = Column(DateTime, default=datetime.utcnow)
    type = Column(String, default="birthday")  # birthday or reminder

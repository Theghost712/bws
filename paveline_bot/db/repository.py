from datetime import datetime
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import config
from .models import Base, Birthday, SentLog, User


class Repository:
    def __init__(self):
        self.engine = create_engine(config.DB_URL, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def add_user(self, telegram_id: str, username: Optional[str] = None, first_name: Optional[str] = None) -> User:
        with self.get_session() as session:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                user = User(telegram_id=telegram_id, username=username, first_name=first_name)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user

    def add_birthday(self, user_id: int, name: str, day: int, month: int, year: Optional[int] = None,
                     relationship: str = "friend", language: str = "en", style: str = "heartfelt",
                     remind: bool = True, remind_days_before: int = 1, chat_id: Optional[str] = None) -> Birthday:
        with self.get_session() as session:
            birthday = Birthday(
                user_id=user_id,
                name=name,
                day=day,
                month=month,
                year=year,
                relationship=relationship,
                language=language,
                style=style,
                remind=remind,
                remind_days_before=remind_days_before,
                chat_id=chat_id or str(user_id),
            )
            session.add(birthday)
            session.commit()
            session.refresh(birthday)
            return birthday

    def get_sent(self, birthday_id: int, kind: str = "birthday"):
        with self.get_session() as session:
            return session.query(SentLog).filter(
                SentLog.birthday_id == birthday_id,
                SentLog.type == kind,
            ).first()

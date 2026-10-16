import logging
from datetime import datetime, timedelta
from typing import List

from .. import config
from ..db import models as db_models
from ..db.repository import Repository

logger = logging.getLogger(__name__)


class SchedulerJobs:
    """Daily jobs for birthday wishes and reminders."""

    def __init__(self):
        self.repo = Repository()

    def _is_sent_today(self, birthday_id: int, kind: str = "birthday") -> bool:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        with self.repo.get_session() as session:
            existing = (
                session.query(db_models.SentLog)
                .filter(
                    db_models.SentLog.birthday_id == birthday_id,
                    db_models.SentLog.type == kind,
                    db_models.SentLog.sent_date >= today,
                )
                .first()
            )
            return existing is not None

    def mark_sent(self, birthday_id: int, kind: str = "birthday") -> None:
        with self.repo.get_session() as session:
            log = db_models.SentLog(birthday_id=birthday_id, type=kind)
            log.sent_date = datetime.utcnow()
            session.add(log)
            session.commit()

    async def send_birthdays(self) -> int:
        """Send wishes for today's birthdays. Idempotent via sent_log."""
        logger.info("Checking for today's birthdays...")
        sent_count = 0
        with self.repo.get_session() as session:
            birthdays: List[db_models.Birthday] = session.query(db_models.Birthday).all()

        today = datetime.utcnow().date()
        for b in birthdays:
            if b.month != today.month or b.day != today.day:
                continue
            if self._is_sent_today(b.id, "birthday"):
                continue
            # generate wish + card, send, log
            self.mark_sent(b.id, "birthday")
            sent_count += 1
        logger.info(f"Processed {len(birthdays)} birthday records, sent {sent_count} wishes today")
        return sent_count

    async def send_reminders(self, days_before: int = 1) -> int:
        """Send reminders N days before upcoming birthdays."""
        logger.info(f"Sending reminders for birthdays in {days_before} days...")
        sent_count = 0
        with self.repo.get_session() as session:
            birthdays: List[db_models.Birthday] = session.query(db_models.Birthday).all()

        upcoming_date = datetime.utcnow().date() + timedelta(days=days_before)
        for b in birthdays:
            if b.month != upcoming_date.month or b.day != upcoming_date.day:
                continue
            if self._is_sent_today(b.id, "reminder"):
                continue
            self.mark_sent(b.id, "reminder")
            sent_count += 1
        logger.info(f"Sent {sent_count} reminders")
        return sent_count

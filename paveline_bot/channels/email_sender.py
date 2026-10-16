import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from .. import config

logger = logging.getLogger(__name__)


class EmailSender:
    async def send_message(self, to_email: str, text: str, image_path: Optional[str] = None) -> bool:
        if not config.SMTP_HOST:
            return False
        try:
            msg = MIMEMultipart()
            msg["From"] = config.SMTP_FROM
            msg["To"] = to_email
            msg["Subject"] = "Birthday Wish"
            msg.attach(MIMEText(text, "plain"))
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
                if config.SMTP_USE_TLS:
                    server.starttls()
                if config.SMTP_USER:
                    server.login(config.SMTP_USER, config.SMTP_PASS)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False

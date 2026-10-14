"""Reminder scheduling logic.

The design is intentionally simple and reliable for a cron-driven workflow:
``send_due_reminders`` walks enabled reminders, works out which ones have a
delivery date of *today*, emails the owner, and stamps ``last_sent_on`` so the
same reminder is never sent twice in a day. Point cron (or a task queue) at the
``send_reminders`` management command once per day.

Swapping in Celery later only requires calling :func:`send_reminder` from a
periodic task instead of the command — the logic below stays the same.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from core.dates import local_today, next_occurrence

from .models import Reminder


def delivery_date(reminder, today=None):
    """The date the reminder should be sent (birthday minus offset)."""
    today = today or local_today()
    birthday = reminder.birthday
    occurrence = next_occurrence(birthday.birthday.month, birthday.birthday.day, today)
    return occurrence - timezone.timedelta(days=reminder.offset_days)


def is_due(reminder, today=None):
    today = today or local_today()
    if not reminder.is_enabled:
        return False
    if reminder.last_sent_on == today:
        return False
    return delivery_date(reminder, today) == today


def due_reminders(today=None):
    today = today or local_today()
    return [reminder for reminder in Reminder.objects.filter(is_enabled=True).select_related("birthday", "user") if is_due(reminder, today)]


def send_reminder(reminder, today=None):
    """Send one reminder email. Returns True when the message was handed off.

    We only stamp ``last_sent_on`` when ``send_mail`` reports at least one
    recipient, so a failed send is retried on the next run rather than being
    silently dropped.
    """
    today = today or local_today()
    user = reminder.user
    recipient_email = user.email
    if not recipient_email:
        return False

    birthday = reminder.birthday
    when = delivery_date(reminder, today)
    days = reminder.offset_days
    if days == 0:
        timing = "today"
    elif days == 1:
        timing = "tomorrow"
    else:
        timing = f"in {days} days"

    subject = f"Birthday reminder: {birthday.recipient_name} is {timing}"
    body = (
        f"Hi {user.get_short_name() or user.username},\n\n"
        f"{birthday.recipient_name}'s birthday is {timing} "
        f"({birthday.birthday:%d %B}).\n\n"
        "Sign in to Paveline to prepare a birthday wish or card:\n"
        f"{getattr(settings, 'SITE_BASE_URL', 'http://127.0.0.1:8000')}\n\n"
        "— Paveline"
    )

    sent = send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=True,
    )
    if sent:
        reminder.last_sent_on = today
        reminder.save(update_fields=["last_sent_on", "updated_at"])
        return True
    return False

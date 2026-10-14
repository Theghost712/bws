from django.conf import settings
from django.db import models

from core.constants import REMINDER_OFFSET_CHOICES


class Reminder(models.Model):
    """A per-birthday email reminder preference.

    ``last_sent_on`` records the calendar date the reminder was last emailed so
    the scheduling command never sends the same reminder twice on one day.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    birthday = models.ForeignKey(
        "birthdays.Birthday",
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    offset_days = models.PositiveSmallIntegerField(choices=REMINDER_OFFSET_CHOICES, default=1)
    is_enabled = models.BooleanField(default=True)
    last_sent_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["birthday__recipient_name", "offset_days"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "birthday", "offset_days"],
                name="unique_reminder_offset_per_birthday",
            )
        ]
        indexes = [models.Index(fields=["user", "is_enabled"])]

    def __str__(self):
        return f"{self.birthday.recipient_name} — {self.get_offset_days_display()}"

    @property
    def recipient_name(self):
        return self.birthday.recipient_name

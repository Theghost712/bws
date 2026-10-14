from django.conf import settings
from django.db import models

from core.constants import LANGUAGE_CODES


class Profile(models.Model):
    """Extra preferences attached to Django's built-in User.

    We deliberately reuse ``django.contrib.auth.models.User`` instead of a
    custom user model so authentication, permissions and the admin all keep
    working out of the box. Profile holds only optional preferences.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=80, blank=True)
    preferred_language = models.CharField(max_length=5, choices=[(c, c) for c in LANGUAGE_CODES], default="en")
    email_reminders = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    @property
    def name(self):
        return self.display_name or self.user.get_full_name() or self.user.username

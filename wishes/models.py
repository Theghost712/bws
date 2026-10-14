from django.conf import settings
from django.db import models
from django.urls import reverse

from core.constants import LANGUAGE_CODES, RELATIONSHIP_CHOICES, TONE_CHOICES


class BirthdayWish(models.Model):
    """A wish a registered user chose to save.

    Anonymous visitors can generate wishes freely; nothing is written to the
    database until a logged-in user explicitly saves one.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishes",
    )
    recipient_name = models.CharField(max_length=60, blank=True)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default="friend")
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default="heartfelt")
    language = models.CharField(max_length=5, choices=[(c, c) for c in LANGUAGE_CODES], default="en")
    length = models.CharField(max_length=10, default="medium")
    sender_name = models.CharField(max_length=60, blank=True)
    personal_message = models.TextField(blank=True)
    message = models.TextField()
    note = models.TextField(blank=True, help_text="Your own private note about this wish.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
            models.Index(fields=["owner", "language"]),
        ]

    def __str__(self):
        return f"Wish for {self.recipient_name}"

    def get_absolute_url(self):
        return reverse("wishes:saved_detail", args=[self.pk])

    def share_text(self):
        return f"{self.heading}\n\n{self.message}\n\n{self.signoff}"

    @property
    def heading(self):
        from .messages import HELLO

        name = self.recipient_name or self.get_relationship_display()
        return f"{HELLO.get(self.language, HELLO['en'])}, {name}!"

    @property
    def signoff(self):
        from .messages import SIGNOFF

        base = SIGNOFF.get(self.language, SIGNOFF["en"])
        return f"{base}, {self.sender_name}" if self.sender_name else base


class Favorite(models.Model):
    """A saved wish a user has starred, kept separate to allow quick toggles."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    wish = models.ForeignKey(
        BirthdayWish,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "wish"], name="unique_favorite_per_user"),
        ]
        indexes = [models.Index(fields=["user", "-created_at"])]

    def __str__(self):
        return f"{self.user.username} ★ {self.wish}"

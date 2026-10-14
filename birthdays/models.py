from django.conf import settings
from django.db import models
from django.urls import reverse

from core.constants import RELATIONSHIP_CHOICES

# Sentinels/documentation:
# ``birthday`` always stores a full date because Django's DateField requires a
# year. When the user does not know the birth year we store the leap-year
# placeholder 1904 here and leave ``birth_year`` empty. All age wording and the
# "next birthday" calculations rely on ``birth_year`` — never on the stored
# placeholder — so an unknown year can never leak an age.
UNKNOWN_YEAR_PLACEHOLDER = 1904


class Birthday(models.Model):
    """A birthday a registered user saved for later reference or reminders."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="birthdays",
    )
    recipient_name = models.CharField(max_length=80)
    birthday = models.DateField()
    birth_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Leave empty when the year is unknown.",
    )
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default="friend")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["recipient_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "recipient_name", "birthday"],
                name="unique_birthday_per_owner",
            )
        ]
        indexes = [
            models.Index(fields=["owner", "recipient_name"]),
        ]

    def __str__(self):
        return f"{self.recipient_name} — {self.birthday:%d %b}"

    def get_absolute_url(self):
        return reverse("birthdays:detail", args=[self.pk])

    @property
    def has_known_year(self):
        return self.birth_year is not None

    def save(self, *args, **kwargs):
        # Keep the placeholder year in sync when the real year is not known.
        target_year = self.birth_year or UNKNOWN_YEAR_PLACEHOLDER
        if self.birthday.year != target_year:
            try:
                self.birthday = self.birthday.replace(year=target_year)
            except ValueError:
                # 29 February in a non-leap target year: keep the placeholder.
                self.birthday = self.birthday.replace(year=UNKNOWN_YEAR_PLACEHOLDER)
        super().save(*args, **kwargs)

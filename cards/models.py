from django.db import models

from core.constants import CARD_CATEGORY_CHOICES, ORIENTATION_CHOICES


class CardTemplate(models.Model):
    """A design the card generator can render.

    Templates are seeded by a data migration so the gallery is never empty,
    and staff can add or disable designs from the admin.
    """

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CARD_CATEGORY_CHOICES, default="colorful")
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES, default="landscape")
    background = models.CharField(max_length=7, default="#f8dfc6", help_text="Hex colour, e.g. #f8dfc6")
    background_secondary = models.CharField(max_length=7, default="#ecd5dc")
    accent = models.CharField(max_length=7, default="#bd685f")
    text_color = models.CharField(max_length=7, default="#4b3142")
    description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [models.Index(fields=["is_active", "sort_order"])]

    def __str__(self):
        return self.name

    @property
    def is_rtl_friendly(self):
        return True

from django.db import migrations

TEMPLATES = [
    {
        "slug": "romantic-blush",
        "name": "Romantic Blush",
        "category": "romantic",
        "orientation": "landscape",
        "background": "#f8dfc6",
        "background_secondary": "#ecd5dc",
        "accent": "#bd685f",
        "text_color": "#4b3142",
        "description": "Soft blush tones for the one you love.",
        "sort_order": 1,
    },
    {
        "slug": "floral-garden",
        "name": "Floral Garden",
        "category": "floral",
        "orientation": "landscape",
        "background": "#e3ecdb",
        "background_secondary": "#cddbc9",
        "accent": "#698468",
        "text_color": "#344d42",
        "description": "A gentle garden of greens and petals.",
        "sort_order": 2,
    },
    {
        "slug": "colorful-celebration",
        "name": "Colorful Celebration",
        "category": "colorful",
        "orientation": "landscape",
        "background": "#fff3d6",
        "background_secondary": "#ffe0e6",
        "accent": "#e07a5f",
        "text_color": "#3d2b3d",
        "description": "Bright and joyful, made for a party.",
        "sort_order": 3,
    },
    {
        "slug": "elegant-midnight",
        "name": "Elegant Midnight",
        "category": "elegant",
        "orientation": "portrait",
        "background": "#2e2a3f",
        "background_secondary": "#4b4166",
        "accent": "#d9b56a",
        "text_color": "#f5eee5",
        "description": "Deep tones with a golden accent.",
        "sort_order": 4,
    },
    {
        "slug": "minimalist-linen",
        "name": "Minimalist Linen",
        "category": "minimalist",
        "orientation": "landscape",
        "background": "#f7f5f2",
        "background_secondary": "#eae6e1",
        "accent": "#8a7f74",
        "text_color": "#33302c",
        "description": "Clean, calm and understated.",
        "sort_order": 5,
    },
    {
        "slug": "children-sky",
        "name": "Children's Sky",
        "category": "children",
        "orientation": "landscape",
        "background": "#d9f0ff",
        "background_secondary": "#ffe6f0",
        "accent": "#3aa0d1",
        "text_color": "#2b3a4a",
        "description": "Playful pastels for little ones.",
        "sort_order": 6,
    },
    {
        "slug": "religious-blessing",
        "name": "Blessing",
        "category": "religious",
        "orientation": "landscape",
        "background": "#efe6d8",
        "background_secondary": "#e6d9c6",
        "accent": "#9c7a3c",
        "text_color": "#4a3a20",
        "description": "Warm and reverent with a golden accent.",
        "sort_order": 7,
    },
    {
        "slug": "professional-slate",
        "name": "Professional Slate",
        "category": "professional",
        "orientation": "landscape",
        "background": "#eef2f7",
        "background_secondary": "#dfe7f1",
        "accent": "#3b6ea5",
        "text_color": "#22303f",
        "description": "A refined choice for colleagues.",
        "sort_order": 8,
    },
]


def seed(apps, schema_editor):
    CardTemplate = apps.get_model("cards", "CardTemplate")
    for entry in TEMPLATES:
        CardTemplate.objects.update_or_create(slug=entry["slug"], defaults=entry)


def unseed(apps, schema_editor):
    CardTemplate = apps.get_model("cards", "CardTemplate")
    CardTemplate.objects.filter(slug__in=[entry["slug"] for entry in TEMPLATES]).delete()


class Migration(migrations.Migration):
    dependencies = [("cards", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]

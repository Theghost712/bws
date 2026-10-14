from django import forms

from core.constants import (
    LANGUAGE_CODES,
    LENGTH_CHOICES,
    RELATIONSHIP_CHOICES,
    SUPPORTED_LANGUAGES,
    TONE_CHOICES,
)
from core.dates import make_date

from .models import BirthdayWish

MONTH_CHOICES = [
    (1, "January"), (2, "February"), (3, "March"), (4, "April"),
    (5, "May"), (6, "June"), (7, "July"), (8, "August"),
    (9, "September"), (10, "October"), (11, "November"), (12, "December"),
]

_INPUT = "form-control"
_SELECT = "form-select"


class WishRequestForm(forms.Form):
    name = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={"class": _INPUT, "placeholder": "e.g. Amina", "autocomplete": "off"}),
    )
    relationship = forms.ChoiceField(
        choices=RELATIONSHIP_CHOICES,
        initial="friend",
        widget=forms.Select(attrs={"class": _SELECT}),
    )
    tone = forms.ChoiceField(
        choices=TONE_CHOICES,
        initial="heartfelt",
        widget=forms.Select(attrs={"class": _SELECT}),
    )
    length = forms.ChoiceField(
        choices=LENGTH_CHOICES,
        initial="medium",
        widget=forms.Select(attrs={"class": _SELECT}),
    )
    language = forms.ChoiceField(
        choices=[(lang["code"], lang["name"]) for lang in SUPPORTED_LANGUAGES],
        initial="en",
        widget=forms.Select(attrs={"class": _SELECT}),
    )
    sender = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={"class": _INPUT, "placeholder": "Your name (optional)", "autocomplete": "off"}),
    )
    personal = forms.CharField(
        max_length=400,
        required=False,
        widget=forms.Textarea(attrs={"class": _INPUT, "rows": 3, "placeholder": "Add a personal line (optional)"}),
    )
    birth_month = forms.ChoiceField(
        choices=[("", "Month")] + MONTH_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": _SELECT}),
    )
    birth_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        required=False,
        widget=forms.NumberInput(attrs={"class": _INPUT, "placeholder": "Day", "min": 1, "max": 31}),
    )
    birth_year = forms.IntegerField(
        min_value=1900,
        max_value=2100,
        required=False,
        widget=forms.NumberInput(attrs={"class": _INPUT, "placeholder": "Year (optional)", "min": 1900, "max": 2100}),
    )
    include_age = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean(self):
        cleaned = super().clean()
        month = cleaned.get("birth_month")
        day = cleaned.get("birth_day")
        if day and not month:
            self.add_error("birth_month", "Choose a month for the birthday.")
        if month and day:
            try:
                make_date(2000, int(month), int(day))
            except (TypeError, ValueError):
                self.add_error("birth_day", "That day does not exist for the selected month.")
        year = cleaned.get("birth_year")
        include = cleaned.get("include_age")
        if include and not year:
            self.add_error("birth_year", "Enter a birth year to include age wording.")
        return cleaned

    def generation_context(self):
        """Build the keyword arguments accepted by the generator service."""
        data = self.cleaned_data
        return {
            "name": data.get("name", ""),
            "relationship": data.get("relationship"),
            "tone": data.get("tone"),
            "length": data.get("length"),
            "language": data.get("language"),
            "sender": data.get("sender", ""),
            "personal": data.get("personal", ""),
            "birth_month": int(data["birth_month"]) if data.get("birth_month") else None,
            "birth_day": data.get("birth_day"),
            "birth_year": data.get("birth_year"),
            "include_age": data.get("include_age", False),
        }


class SavedWishForm(forms.ModelForm):
    class Meta:
        model = BirthdayWish
        fields = [
            "recipient_name", "relationship", "tone", "language", "length",
            "sender_name", "personal_message", "message", "note",
        ]
        widgets = {
            "recipient_name": forms.TextInput(attrs={"class": _INPUT}),
            "relationship": forms.Select(attrs={"class": _SELECT}),
            "tone": forms.Select(attrs={"class": _SELECT}),
            "language": forms.Select(attrs={"class": _SELECT}),
            "length": forms.Select(attrs={"class": _SELECT}),
            "sender_name": forms.TextInput(attrs={"class": _INPUT}),
            "personal_message": forms.Textarea(attrs={"class": _INPUT, "rows": 3}),
            "message": forms.Textarea(attrs={"class": _INPUT, "rows": 5}),
            "note": forms.Textarea(attrs={"class": _INPUT, "rows": 2}),
        }


class WishNoteForm(forms.ModelForm):
    class Meta:
        model = BirthdayWish
        fields = ["note"]
        widgets = {"note": forms.Textarea(attrs={"class": _INPUT, "rows": 3})}

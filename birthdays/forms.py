from django import forms

from core.constants import RELATIONSHIP_CHOICES
from core.dates import make_date

from .models import UNKNOWN_YEAR_PLACEHOLDER, Birthday

MONTH_CHOICES = [
    (1, "January"), (2, "February"), (3, "March"), (4, "April"),
    (5, "May"), (6, "June"), (7, "July"), (8, "August"),
    (9, "September"), (10, "October"), (11, "November"), (12, "December"),
]


class BirthdayForm(forms.ModelForm):
    """Form that accepts a birthday as month/day plus an optional year."""

    birth_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    birth_day = forms.IntegerField(
        min_value=1,
        max_value=31,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 31}),
    )
    birth_year = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2100,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Optional"}),
        help_text="Leave empty if you do not know the birth year.",
    )

    class Meta:
        model = Birthday
        fields = ["recipient_name", "relationship", "notes"]
        widgets = {
            "recipient_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Their name"}),
            "relationship": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Gift ideas, reminders, anything useful..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["birth_month"].initial = self.instance.birthday.month
            self.fields["birth_day"].initial = self.instance.birthday.day
            self.fields["birth_year"].initial = self.instance.birth_year

    def clean(self):
        cleaned = super().clean()
        month = cleaned.get("birth_month")
        day = cleaned.get("birth_day")
        year = cleaned.get("birth_year")
        if month and day:
            try:
                cleaned["_birthday"] = make_date(year or UNKNOWN_YEAR_PLACEHOLDER, int(month), int(day))
            except (TypeError, ValueError):
                self.add_error("birth_day", "That day does not exist for the selected month.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.birthday = self.cleaned_data["_birthday"]
        instance.birth_year = self.cleaned_data.get("birth_year") or None
        if commit:
            instance.save()
        return instance

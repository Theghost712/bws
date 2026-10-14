from django import forms

from core.constants import REMINDER_OFFSET_CHOICES

from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["birthday", "offset_days", "is_enabled"]
        widgets = {
            "birthday": forms.Select(attrs={"class": "form-select"}),
            "offset_days": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["offset_days"].choices = REMINDER_OFFSET_CHOICES
        if user is not None:
            self.fields["birthday"].queryset = user.birthdays.all()
        self.fields["is_enabled"].widget.attrs.update({"class": "form-check-input"})

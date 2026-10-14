from django import forms

from core.constants import ORIENTATION_CHOICES, SUPPORTED_LANGUAGES

from .models import CardTemplate
from .services import FONT_CHOICES, validate_upload


class CardDesignForm(forms.Form):
    template = forms.ModelChoiceField(
        queryset=CardTemplate.objects.filter(is_active=True),
        to_field_name="slug",
        widget=forms.Select(attrs={"class": "form-select", "id": "id_template"}),
    )
    language = forms.ChoiceField(
        choices=[(lang["code"], lang["name"]) for lang in SUPPORTED_LANGUAGES],
        initial="en",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    recipient_name = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Amina"}),
    )
    message = forms.CharField(
        max_length=600,
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 4, "id": "id_message",
                   "placeholder": "Write the birthday message you want on the card"}
        ),
    )
    sender_name = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name (optional)"}),
    )
    font = forms.ChoiceField(
        choices=FONT_CHOICES,
        initial="serif",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    accent = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "color", "value": "#bd685f"}),
    )
    orientation = forms.ChoiceField(
        choices=ORIENTATION_CHOICES,
        initial="landscape",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        help_text="Optional. JPG, PNG, WEBP or GIF up to 5 MB.",
    )
    heading = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Happy birthday, Amina!"}),
        help_text="Leave blank to use a friendly default greeting.",
    )

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        ok, error = validate_upload(photo)
        if not ok:
            raise forms.ValidationError(error)
        return photo

    def clean_accent(self):
        accent = (self.cleaned_data.get("accent") or "").strip()
        if accent and not (accent.startswith("#") and len(accent) == 7):
            raise forms.ValidationError("Use a hex colour such as #bd685f.")
        return accent or "#bd685f"

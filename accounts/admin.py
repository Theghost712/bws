from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "preferred_language", "email_reminders", "updated_at")
    list_filter = ("preferred_language", "email_reminders")
    search_fields = ("user__username", "user__email", "display_name")
    autocomplete_fields = ("user",)

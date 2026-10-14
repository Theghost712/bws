from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("birthday", "user", "offset_days", "is_enabled", "last_sent_on")
    list_filter = ("offset_days", "is_enabled")
    search_fields = ("birthday__recipient_name", "user__username")
    raw_id_fields = ("user", "birthday")

from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "is_handled", "created_at")
    list_filter = ("is_handled", "created_at")
    search_fields = ("subject", "name", "email", "message")
    date_hierarchy = "created_at"
    list_editable = ("is_handled",)

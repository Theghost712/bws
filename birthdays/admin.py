from django.contrib import admin

from .models import Birthday


@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ("recipient_name", "owner", "birthday", "birth_year", "relationship", "updated_at")
    list_filter = ("relationship", "birth_year")
    search_fields = ("recipient_name", "notes", "owner__username")
    date_hierarchy = "birthday"
    raw_id_fields = ("owner",)

from django.contrib import admin

from .models import CardTemplate


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "orientation", "is_active", "sort_order")
    list_filter = ("category", "orientation", "is_active")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active", "sort_order")

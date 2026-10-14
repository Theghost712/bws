from django.contrib import admin

from .models import BirthdayWish, Favorite


@admin.register(BirthdayWish)
class BirthdayWishAdmin(admin.ModelAdmin):
    list_display = ("recipient_name", "owner", "language", "tone", "relationship", "created_at")
    list_filter = ("language", "tone", "relationship", "created_at")
    search_fields = ("recipient_name", "sender_name", "message", "owner__username")
    date_hierarchy = "created_at"
    raw_id_fields = ("owner",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "wish", "created_at")
    search_fields = ("user__username", "wish__recipient_name")
    raw_id_fields = ("user", "wish")

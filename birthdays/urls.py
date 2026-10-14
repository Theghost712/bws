from django.urls import path

from . import views

app_name = "birthdays"

urlpatterns = [
    path("", views.birthday_list, name="list"),
    path("add/", views.birthday_add, name="add"),
    path("upcoming/", views.birthday_upcoming, name="upcoming"),
    path("<int:pk>/", views.birthday_detail, name="detail"),
    path("<int:pk>/edit/", views.birthday_edit, name="edit"),
    path("<int:pk>/delete/", views.birthday_delete, name="delete"),
]

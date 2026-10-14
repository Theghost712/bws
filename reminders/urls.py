from django.urls import path

from . import views

app_name = "reminders"

urlpatterns = [
    path("", views.reminder_list, name="list"),
    path("add/", views.reminder_add, name="add"),
    path("<int:pk>/edit/", views.reminder_edit, name="edit"),
    path("<int:pk>/toggle/", views.reminder_toggle, name="toggle"),
    path("<int:pk>/delete/", views.reminder_delete, name="delete"),
]

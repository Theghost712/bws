from django.urls import path

from . import views

app_name = "wishes"

urlpatterns = [
    path("create/", views.create, name="create"),
    path("result/", views.result, name="result"),
    path("save/", views.save_wish, name="save"),
    path("saved/", views.saved_list, name="saved_list"),
    path("saved/<int:pk>/", views.saved_detail, name="saved_detail"),
    path("saved/<int:pk>/edit/", views.saved_edit, name="saved_edit"),
    path("saved/<int:pk>/delete/", views.saved_delete, name="saved_delete"),
    path("saved/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/", views.favorites_list, name="favorites"),
]

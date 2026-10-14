from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("design/", views.designer, name="designer"),
    path("render/", views.render_image, name="render"),
    path("preview/<slug:slug>.png", views.template_preview, name="template_preview"),
]

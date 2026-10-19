from django.urls import path

from . import views

app_name = "portfolios"

urlpatterns = [
    path("", views.obedi_portfolio, name="obedi"),
]

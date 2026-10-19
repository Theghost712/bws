"""Root URL configuration for the Paveline platform."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import SITEMAPS
from core.views import robots_txt

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("wishes/", include("wishes.urls")),
    path("cards/", include("cards.urls")),
    path("birthdays/", include("birthdays.urls")),
    path("reminders/", include("reminders.urls")),
    path("portfolios/", include("portfolios.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

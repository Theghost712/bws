"""Sitemap definitions for search engines.

Only publicly reachable pages are listed. Authenticated areas (dashboard,
saved wishes, birthdays, reminders, admin) are intentionally excluded.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Public, canonically addressable pages."""

    protocol = "https"
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "core:home",
            "cards:gallery",
            "wishes:create",
            "cards:designer",
            "core:about",
            "core:contact",
            "core:privacy",
            "core:terms",
        ]

    def location(self, item):
        return reverse(item)


SITEMAPS = {"static": StaticViewSitemap}

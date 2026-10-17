import hmac
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from birthdays.models import Birthday
from birthdays.services import upcoming_birthdays
from cards.models import CardTemplate
from reminders.models import Reminder
from wishes.forms import WishRequestForm
from wishes.models import BirthdayWish, Favorite

from .constants import RELATIONSHIP_CHOICES, TONE_CHOICES
from .forms import ContactForm

# Homepage category chips. Each one simply points at the generator with a
# sensible tone/relationship preselected so visitors can start in one tap.
WISH_CATEGORIES = [
    {"slug": "romantic", "label": "Romantic", "icon": "♥", "tone": "romantic", "relationship": "wife"},
    {"slug": "friends", "label": "Friends", "icon": "✌", "tone": "funny", "relationship": "friend"},
    {"slug": "family", "label": "Family", "icon": "⌂", "tone": "heartfelt", "relationship": "relative"},
    {"slug": "parents", "label": "Parents", "icon": "✿", "tone": "emotional", "relationship": "mother"},
    {"slug": "children", "label": "Children", "icon": "★", "tone": "creative", "relationship": "son"},
    {"slug": "professional", "label": "Professional", "icon": "▤", "tone": "formal", "relationship": "colleague"},
    {"slug": "funny", "label": "Funny", "icon": "☺", "tone": "funny", "relationship": "friend"},
    {"slug": "emotional", "label": "Emotional", "icon": "❥", "tone": "emotional", "relationship": "friend"},
    {"slug": "inspirational", "label": "Inspirational", "icon": "✧", "tone": "inspirational", "relationship": "friend"},
    {"slug": "religious", "label": "Religious", "icon": "✟", "tone": "religious", "relationship": "friend"},
]


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quick_form"] = WishRequestForm(initial={"language": self.request.LANGUAGE_CODE})
        context["card_templates"] = CardTemplate.objects.filter(is_active=True)[:6]
        context["categories"] = WISH_CATEGORIES
        context["relationship_count"] = len(RELATIONSHIP_CHOICES)
        context["tone_count"] = len(TONE_CHOICES)
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@login_required
def dashboard(request):
    today = timezone.localdate()
    birthdays = Birthday.objects.filter(owner=request.user)
    context = {
        "birthday_count": birthdays.count(),
        "today_birthdays": birthdays.filter(birthday__month=today.month, birthday__day=today.day),
        "upcoming": upcoming_birthdays(request.user, limit=5),
        "wish_count": BirthdayWish.objects.filter(owner=request.user).count(),
        "favorite_count": Favorite.objects.filter(user=request.user).count(),
        "reminder_count": Reminder.objects.filter(user=request.user, is_enabled=True).count(),
        "recent_wishes": BirthdayWish.objects.filter(owner=request.user)[:4],
    }
    return render(request, "core/dashboard.html", context)


@require_GET
def send_reminders_cron(request):
    """Endpoint hit by the Vercel Cron job to send due birthday reminders.

    Vercel sends ``Authorization: Bearer <CRON_SECRET>`` on cron requests when
    the ``CRON_SECRET`` environment variable is set. We require that secret so
    the endpoint cannot be triggered by the public.
    """
    expected = os.environ.get("CRON_SECRET")
    if not expected:
        return HttpResponseForbidden("CRON_SECRET not configured")

    supplied = request.headers.get("Authorization", "")
    if not hmac.compare_digest(supplied, f"Bearer {expected}"):
        return HttpResponseForbidden("Forbidden")

    from io import StringIO

    out = StringIO()
    call_command("send_reminders", stdout=out)
    return HttpResponse(out.getvalue(), content_type="text/plain")


@require_GET
def robots_txt(request):
    """Serve ``/robots.txt`` with crawl rules and the sitemap location."""
    sitemap_url = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /birthdays/",
        "Disallow: /reminders/",
        "Disallow: /wishes/saved/",
        "Disallow: /wishes/favorites/",
        "Disallow: /cards/render/",
        "Disallow: /cron/",
        "",
        f"Sitemap: {sitemap_url}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

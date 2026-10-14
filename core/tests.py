from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class PublicPageTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Make Every Birthday")

    def test_static_pages(self):
        for name in ["core:about", "core:privacy", "core:terms"]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_contact_get(self):
        self.assertEqual(self.client.get(reverse("core:contact")).status_code, 200)

    def test_contact_details_shown(self):
        response = self.client.get(reverse("core:contact"))
        self.assertContains(response, "menyendoyemigaru@gmail.com")
        self.assertContains(response, "tel:+255747433510")
        self.assertContains(response, "+255 747 433 510")

    def test_footer_contact_details(self):
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "mailto:menyendoyemigaru@gmail.com")

    def test_contact_post_creates_message(self):
        response = self.client.post(
            reverse("core:contact"),
            {"name": "Amina", "email": "amina@example.com", "subject": "Hello", "message": "A useful hello message."},
        )
        self.assertRedirects(response, reverse("core:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_post_requires_valid_message(self):
        response = self.client.post(
            reverse("core:contact"),
            {"name": "Amina", "email": "amina@example.com", "subject": "Hi", "message": "short"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertFormError(response.context["form"], "message", "Please write at least 10 characters so we can help.")


class DashboardTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_dashboard_loads_for_user(self):
        user = User.objects.create_user("tester", password="pass12345")
        self.client.force_login(user)
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)


class LanguageTests(TestCase):
    def test_set_language_persists(self):
        response = self.client.post(reverse("set_language"), {"language": "fr", "next": "/"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies["django_language"].value, "fr")

    def test_rtl_language_sets_dir(self):
        self.client.post(reverse("set_language"), {"language": "ar", "next": "/"})
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, 'dir="rtl"')

    def test_catalogs_translate_ui(self):
        response = self.client.get(reverse("core:home"), headers={"accept-language": "fr"})
        self.assertContains(response, "Accueil")
        response = self.client.get(reverse("core:home"), headers={"accept-language": "sw"})
        self.assertContains(response, "Nyumbani")

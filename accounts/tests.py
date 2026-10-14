from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Profile


class RegistrationTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "amina", "first_name": "Amina", "email": "amina@example.com",
                "password1": "Str0ngPass!23", "password2": "Str0ngPass!23",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="amina").exists())
        self.assertTrue(Profile.objects.filter(user__username="amina").exists())

    def test_duplicate_email_rejected(self):
        User.objects.create_user("first", email="dup@example.com", password="pass12345")
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "second", "email": "dup@example.com",
                "password1": "Str0ngPass!23", "password2": "Str0ngPass!23",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)

    def test_password_validation(self):
        response = self.client.post(
            reverse("accounts:register"),
            {"username": "weak", "email": "weak@example.com", "password1": "short", "password2": "short"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("amina", password="Str0ngPass!23")

    def test_login(self):
        response = self.client.post(reverse("accounts:login"), {"username": "amina", "password": "Str0ngPass!23"})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:profile"),
            {"display_name": "Amina", "first_name": "Amina", "email": "a@example.com", "preferred_language": "sw", "email_reminders": "on"},
        )
        self.assertEqual(response.status_code, 302)
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.display_name, "Amina")
        self.assertEqual(profile.preferred_language, "sw")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetTests(TestCase):
    def test_password_reset_sends_email(self):
        User.objects.create_user("amina", email="amina@example.com", password="Str0ngPass!23")
        response = self.client.post(reverse("accounts:password_reset"), {"email": "amina@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

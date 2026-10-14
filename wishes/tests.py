from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.constants import LANGUAGE_CODES, TONE_CHOICES

from .models import BirthdayWish, Favorite
from .services import as_share_text, generate_alternatives, generate_wish


class GeneratorServiceTests(TestCase):
    def test_all_languages_and_tones_produce_text(self):
        for language in LANGUAGE_CODES:
            for tone, _ in TONE_CHOICES:
                with self.subTest(language=language, tone=tone):
                    wish = generate_wish(name="Amina", language=language, tone=tone)
                    self.assertTrue(wish["message"].strip())
                    self.assertIn("Amina", wish["heading"])

    def test_lengths_differ(self):
        short = generate_wish(name="Amina", length="short")
        long = generate_wish(name="Amina", length="long")
        self.assertLessEqual(len(short["message"]), len(long["message"]))

    def test_uses_name_and_sender(self):
        wish = generate_wish(name="Amina", sender="Juma")
        self.assertIn("Amina", wish["heading"])
        self.assertIn("Juma", wish["signoff"])

    def test_personal_message_included(self):
        wish = generate_wish(name="Amina", personal="You are the best sister.")
        self.assertIn("You are the best sister.", wish["message"])

    def test_relationship_reflected_when_name_missing(self):
        wish = generate_wish(name="", relationship="mother", language="en")
        self.assertIn("Mum", wish["heading"])

    def test_age_never_shown_without_birth_year(self):
        wish = generate_wish(name="Amina", birth_month=1, birth_day=1, include_age=True)
        self.assertIsNone(wish["age"])

    def test_age_shown_with_birth_year(self):
        wish = generate_wish(
            name="Amina", birth_month=1, birth_day=1, birth_year=2000,
            include_age=True, today=date(2026, 1, 1),
        )
        self.assertEqual(wish["age"], 26)

    def test_is_today_only_on_matching_date(self):
        today = date(2026, 10, 14)
        matching = generate_wish(birth_month=10, birth_day=14, today=today)
        other = generate_wish(birth_month=10, birth_day=15, today=today)
        self.assertTrue(matching["is_today"])
        self.assertFalse(other["is_today"])

    def test_invalid_language_and_tone_fall_back(self):
        wish = generate_wish(language="zz", tone="nonsense")
        self.assertEqual(wish["language"], "en")
        self.assertEqual(wish["tone"], "heartfelt")

    def test_alternatives_are_distinct(self):
        alternatives = generate_alternatives({"name": "Amina"}, count=3)
        messages = {item["message"] for item in alternatives}
        self.assertGreater(len(messages), 1)

    def test_share_text_shape(self):
        wish = generate_wish(name="Amina")
        text = as_share_text(wish)
        self.assertIn(wish["heading"], text)
        self.assertIn(wish["message"], text)


class WishFlowTests(TestCase):
    def test_create_anonymous_redirects_to_result(self):
        response = self.client.post(
            reverse("wishes:create"),
            {
                "name": "Amina", "relationship": "friend", "tone": "funny",
                "length": "medium", "language": "en", "sender": "Juma",
                "personal": "", "include_age": False,
            },
        )
        self.assertRedirects(response, reverse("wishes:result"))
        result = self.client.get(reverse("wishes:result"))
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, "Amina")

    def test_invalid_birth_day_rejected(self):
        response = self.client.post(
            reverse("wishes:create"),
            {
                "name": "Amina", "relationship": "friend", "tone": "funny",
                "length": "medium", "language": "en", "birth_month": "2",
                "birth_day": "30", "include_age": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_include_age_without_year_rejected(self):
        response = self.client.post(
            reverse("wishes:create"),
            {
                "name": "Amina", "relationship": "friend", "tone": "funny",
                "length": "medium", "language": "en", "birth_month": "1",
                "birth_day": "1", "include_age": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("birth_year", response.context["form"].errors)

    def test_result_without_context_redirects(self):
        response = self.client.get(reverse("wishes:result"))
        self.assertRedirects(response, reverse("wishes:create"))


class SavedWishTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345")
        self.other = User.objects.create_user("other", password="pass12345")
        self.wish = BirthdayWish.objects.create(
            owner=self.user, recipient_name="Amina", relationship="friend",
            tone="funny", language="en", length="medium", message="Happy birthday, Amina!",
        )

    def test_save_requires_login(self):
        response = self.client.post(reverse("wishes:save"), {"message": "hi"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_save_creates_wish(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("wishes:save"),
            {
                "recipient_name": "Amina", "relationship": "friend", "tone": "funny",
                "language": "en", "length": "medium", "sender_name": "",
                "personal_message": "", "message": "A lovely wish.", "note": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BirthdayWish.objects.filter(owner=self.user, recipient_name="Amina").exists())

    def test_owner_can_view_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("wishes:saved_detail", args=[self.wish.pk]))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_view(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("wishes:saved_detail", args=[self.wish.pk]))
        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_delete(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse("wishes:saved_delete", args=[self.wish.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(BirthdayWish.objects.filter(pk=self.wish.pk).exists())

    def test_favorite_toggle(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("wishes:toggle_favorite", args=[self.wish.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(user=self.user, wish=self.wish).exists())
        self.client.post(reverse("wishes:toggle_favorite", args=[self.wish.pk]))
        self.assertFalse(Favorite.objects.filter(user=self.user, wish=self.wish).exists())

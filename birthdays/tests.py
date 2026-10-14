from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.dates import next_occurrence

from .models import Birthday
from .services import annotate_birthday, upcoming_birthdays


class DateLogicTests(TestCase):
    def test_leap_year_birthday_maps_to_28_feb(self):
        # 2026 is not a leap year.
        self.assertEqual(next_occurrence(2, 29, date(2026, 2, 27)), date(2026, 2, 28))
        # 2024 is a leap year.
        self.assertEqual(next_occurrence(2, 29, date(2024, 2, 1)), date(2024, 2, 29))

    def test_next_occurrence_rolls_to_next_year(self):
        self.assertEqual(next_occurrence(1, 1, date(2026, 6, 1)), date(2027, 1, 1))


class BirthdayServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345")

    def test_unknown_year_never_exposes_age(self):
        birthday = Birthday.objects.create(
            owner=self.user, recipient_name="Amina", relationship="friend",
            birthday=date(1904, 5, 10), birth_year=None,
        )
        info = annotate_birthday(birthday, today=date(2026, 5, 1))
        self.assertIsNone(info["age_turning"])
        self.assertIsNone(info["current_age"])

    def test_upcoming_sorted_by_days(self):
        Birthday.objects.create(owner=self.user, recipient_name="Later", birthday=date(1904, 12, 1))
        Birthday.objects.create(owner=self.user, recipient_name="Sooner", birthday=date(1904, 11, 1))
        entries = upcoming_birthdays(self.user, today=date(2026, 10, 1))
        self.assertEqual(entries[0]["birthday"].recipient_name, "Sooner")

    def test_birthday_today(self):
        Birthday.objects.create(owner=self.user, recipient_name="Today", birthday=date(1904, 10, 14))
        entries = upcoming_birthdays(self.user, today=date(2026, 10, 14))
        self.assertTrue(entries[0]["is_today"])


class BirthdayViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345")
        self.other = User.objects.create_user("other", password="pass12345")
        self.client.force_login(self.user)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("birthdays:list"))
        self.assertEqual(response.status_code, 302)

    def test_add_birthday(self):
        response = self.client.post(
            reverse("birthdays:add"),
            {"recipient_name": "Amina", "relationship": "friend", "birth_month": "5", "birth_day": "10", "birth_year": "1998", "notes": ""},
        )
        self.assertEqual(response.status_code, 302)
        birthday = Birthday.objects.get(recipient_name="Amina")
        self.assertEqual(birthday.birth_year, 1998)
        self.assertEqual(birthday.birthday.month, 5)
        self.assertEqual(birthday.birthday.day, 10)

    def test_add_birthday_without_year(self):
        self.client.post(
            reverse("birthdays:add"),
            {"recipient_name": "NoYear", "relationship": "friend", "birth_month": "3", "birth_day": "15", "birth_year": "", "notes": ""},
        )
        birthday = Birthday.objects.get(recipient_name="NoYear")
        self.assertIsNone(birthday.birth_year)

    def test_invalid_day_rejected(self):
        response = self.client.post(
            reverse("birthdays:add"),
            {"recipient_name": "Bad", "relationship": "friend", "birth_month": "2", "birth_day": "30", "birth_year": "", "notes": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Birthday.objects.filter(recipient_name="Bad").exists())

    def test_edit_birthday(self):
        birthday = Birthday.objects.create(owner=self.user, recipient_name="Amina", birthday=date(1904, 5, 10))
        self.client.post(
            reverse("birthdays:edit", args=[birthday.pk]),
            {"recipient_name": "Amina B", "relationship": "sister", "birth_month": "5", "birth_day": "10", "birth_year": "", "notes": "note"},
        )
        birthday.refresh_from_db()
        self.assertEqual(birthday.recipient_name, "Amina B")

    def test_delete_birthday(self):
        birthday = Birthday.objects.create(owner=self.user, recipient_name="Amina", birthday=date(1904, 5, 10))
        response = self.client.post(reverse("birthdays:delete", args=[birthday.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Birthday.objects.filter(pk=birthday.pk).exists())

    def test_cannot_edit_other_users_birthday(self):
        birthday = Birthday.objects.create(owner=self.other, recipient_name="Secret", birthday=date(1904, 5, 10))
        response = self.client.get(reverse("birthdays:edit", args=[birthday.pk]))
        self.assertEqual(response.status_code, 404)

    def test_search_filter(self):
        Birthday.objects.create(owner=self.user, recipient_name="Amina", birthday=date(1904, 5, 10))
        Birthday.objects.create(owner=self.user, recipient_name="Juma", birthday=date(1904, 6, 10))
        response = self.client.get(reverse("birthdays:list"), {"q": "Amina"})
        self.assertContains(response, "Amina")
        self.assertNotContains(response, "Juma")

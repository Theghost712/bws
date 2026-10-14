from datetime import date
from io import StringIO

from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from birthdays.models import Birthday

from .models import Reminder
from .services import due_reminders, is_due, send_reminder


class ReminderLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345", email="owner@example.com")
        self.birthday = Birthday.objects.create(
            owner=self.user, recipient_name="Amina", relationship="friend", birthday=date(1904, 10, 15),
        )
        self.reminder = Reminder.objects.create(user=self.user, birthday=self.birthday, offset_days=1)

    def test_due_on_correct_day(self):
        self.assertTrue(is_due(self.reminder, today=date(2026, 10, 14)))
        self.assertFalse(is_due(self.reminder, today=date(2026, 10, 13)))

    def test_disabled_reminder_not_due(self):
        self.reminder.is_enabled = False
        self.reminder.save()
        self.assertFalse(is_due(self.reminder, today=date(2026, 10, 14)))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_send_reminder_marks_last_sent(self):
        sent = send_reminder(self.reminder, today=date(2026, 10, 14))
        self.assertTrue(sent)
        self.reminder.refresh_from_db()
        self.assertEqual(self.reminder.last_sent_on, date(2026, 10, 14))
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_no_duplicate_send_same_day(self):
        send_reminder(self.reminder, today=date(2026, 10, 14))
        self.assertFalse(is_due(self.reminder, today=date(2026, 10, 14)))
        self.assertEqual(due_reminders(today=date(2026, 10, 14)), [])

    def test_no_email_address_not_sent(self):
        self.user.email = ""
        self.user.save()
        self.assertFalse(send_reminder(self.reminder, today=date(2026, 10, 14)))


class ReminderCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345", email="owner@example.com")
        self.birthday = Birthday.objects.create(
            owner=self.user, recipient_name="Amina", relationship="friend", birthday=date(1904, 10, 15),
        )
        Reminder.objects.create(user=self.user, birthday=self.birthday, offset_days=1)

    def test_dry_run_lists_reminders(self):
        from unittest import mock

        out = StringIO()
        with mock.patch("reminders.management.commands.send_reminders.local_today", return_value=date(2026, 10, 14)):
            call_command("send_reminders", "--dry-run", stdout=out)
        self.assertIn("would send", out.getvalue())

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_command_sends_email(self):
        # Freeze the service clock by patching local_today through the command.
        from unittest import mock

        with mock.patch("reminders.management.commands.send_reminders.local_today", return_value=date(2026, 10, 14)):
            out = StringIO()
            call_command("send_reminders", stdout=out)
            self.assertIn("sent", out.getvalue())
        self.assertEqual(len(mail.outbox), 1)


class ReminderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass12345", email="owner@example.com")
        self.other = User.objects.create_user("other", password="pass12345")
        self.birthday = Birthday.objects.create(
            owner=self.user, recipient_name="Amina", relationship="friend", birthday=date(1904, 10, 15),
        )
        self.reminder = Reminder.objects.create(user=self.user, birthday=self.birthday, offset_days=1)
        self.client.force_login(self.user)

    def test_list_loads(self):
        self.assertEqual(self.client.get(reverse("reminders:list")).status_code, 200)

    def test_toggle(self):
        self.client.post(reverse("reminders:toggle", args=[self.reminder.pk]))
        self.reminder.refresh_from_db()
        self.assertFalse(self.reminder.is_enabled)

    def test_cannot_access_other_users_reminder(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("reminders:edit", args=[self.reminder.pk]))
        self.assertEqual(response.status_code, 404)

    def test_add_without_birthdays_redirects(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("reminders:add"))
        self.assertRedirects(response, reverse("birthdays:add"))

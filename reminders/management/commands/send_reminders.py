"""Management command that sends due birthday reminders.

Run once per day from cron (or a Celery beat schedule)::

    python manage.py send_reminders

Use ``--dry-run`` to list what would be sent without emailing anyone.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.dates import local_today
from reminders.services import due_reminders, send_reminder


class Command(BaseCommand):
    help = "Send birthday reminder emails that are due today."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List due reminders without sending emails.",
        )

    def handle(self, *args, **options):
        today = local_today()
        reminders = due_reminders(today)
        if not reminders:
            self.stdout.write(self.style.WARNING(f"No reminders due on {today:%Y-%m-%d}."))
            return

        sent = 0
        skipped = 0
        for reminder in reminders:
            label = f"{reminder.user.username} <- {reminder.birthday.recipient_name} ({reminder.get_offset_days_display()})"
            if options["dry_run"]:
                self.stdout.write(f"[dry-run] would send: {label}")
                continue
            if send_reminder(reminder, today):
                sent += 1
                self.stdout.write(self.style.SUCCESS(f"sent: {label}"))
            else:
                skipped += 1
                self.stdout.write(self.style.ERROR(f"failed (will retry): {label}"))

        if not options["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"Done. Sent {sent}, failed {skipped}. ({timezone.now():%Y-%m-%d %H:%M})"))

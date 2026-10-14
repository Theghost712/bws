# Paveline

Paveline is a multilingual birthday-wish and greeting-card platform built with
Django. It generates personalised, natural-sounding birthday messages in
**English, Kiswahili, French, Spanish and Arabic**, renders shareable greeting
cards, and helps registered users keep track of birthdays and reminders.

## Features

- **Wish generator** — five tones (warm, playful, formal, poetic, funny), three
  message lengths, relationship-aware wording, optional personal note and an
  optional age line that is **only** shown when the birth year is known.
- **Native multilingual messages** — English, Kiswahili, French, Spanish and
  Arabic (Arabic rendered right-to-left).
- **Birthday card designer** — server-rendered cards rendered with Pillow,
  optional photo upload, live preview, eight seeded templates, category filter
  and PNG download.
- **Birthday manager** — save birthdays, search, and view upcoming birthdays
  with correct leap-year handling (29 Feb → 28 Feb in non-leap years).
- **Reminders** — email reminders a configurable number of days before each
  birthday, sent via a management command suitable for cron.
- **Accounts & privacy** — generate wishes as a guest; optionally register to
  save wishes, birthdays and reminders. Wish generation never sends recipient
  data anywhere.
- **i18n-ready UI** — every user-facing string is marked for translation with a
  working language switcher (including RTL for Arabic).

## Requirements

- Python 3.11+
- The Python packages in `requirements.txt`
  (`Django`, `python-dotenv`, `Pillow`, and optionally `arabic-reshaper` +
  `python-bidi` for shaped Arabic text on server-rendered cards)

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # then edit values as needed
python manage.py migrate      # also seeds the card templates
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Environment variables

Configuration is read from `.env` via `python-dotenv`. See `.env.example` for
the full list. Key options:

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Secret key (required in production) |
| `DJANGO_DEBUG` | `True`/`False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names |
| `DJANGO_TIME_ZONE` | e.g. `Africa/Nairobi` |
| `SITE_BASE_URL` | Absolute URL used in reminder emails |
| `DB_ENGINE` | Leave unset for SQLite; set `mysql` for MySQL |
| `EMAIL_BACKEND` | Console backend by default; use SMTP in production |

## Card fonts

Card rendering discovers fonts from the usual system paths
(`/usr/share/fonts/truetype/{dejavu,noto,liberation,freefont}`). Arabic card
text is shaped server-side when `arabic-reshaper` and `python-bidi` are
installed; without them, Arabic text still renders (unshaped).

## Reminders

Reminders are sent by a management command, intended to run daily via cron:

```bash
python manage.py send_reminders            # send due reminders
python manage.py send_reminders --dry-run  # list without sending
```

Example crontab entry (08:00 daily):

```cron
0 8 * * * cd /path/to/django-bday && .venv/bin/python manage.py send_reminders >> /var/log/paveline-reminders.log 2>&1
```

## Tests

```bash
python manage.py test
```

The suite covers the wish generator (all languages/tones/lengths, age and
leap-year rules), saved-wish ownership, birthday CRUD and permissions,
card rendering and upload validation, reminder scheduling/deduplication, and
account/authentication flows.

## Internationalization

UI strings are wrapped with `{% translate %}` / `{% blocktrans %}` and wish
content is generated natively per language. To build message catalogs you need
GNU gettext (`gettext` package provides `xgettext`/`msgfmt`):

```bash
python manage.py makemessages -l sw -l fr -l es -l ar
# edit locale/<lang>/LC_MESSAGES/django.po
python manage.py compilemessages
```

Without gettext installed, the language switcher still works and untranslated
strings fall back to English.

## Production notes

- Set `DJANGO_DEBUG=False` and a real `DJANGO_SECRET_KEY`.
- Set `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.
- Use MySQL (`DB_ENGINE=mysql`, install `mysqlclient`) or another managed DB.
- Run `python manage.py collectstatic` and serve static/media from your web
  server or object storage.
- Run the app under a WSGI server such as Gunicorn behind a reverse proxy.

## Project layout

| App | Responsibility |
| --- | --- |
| `core` | Home/marketing pages, contact, shared constants, date + i18n helpers |
| `wishes` | Multilingual wish generation, saving, favorites |
| `cards` | Card templates, Pillow rendering, designer |
| `birthdays` | Birthday manager and upcoming calculations |
| `reminders` | Email reminders and the `send_reminders` command |
| `accounts` | Registration, login, profile and password reset |

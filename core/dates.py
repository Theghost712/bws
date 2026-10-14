"""Date helpers shared by the wish generator and birthday manager.

Leap-year policy
----------------
A birthday entered as 29 February is observed on **28 February** in
non-leap years. This is applied consistently everywhere a "next birthday" is
calculated so upcoming lists and reminders never disagree.
"""

from datetime import date

try:
    from django.utils import timezone
except Exception:  # pragma: no cover - allows the pure helpers to be reused
    timezone = None


def _resolve_day(year, month, day):
    """Return a valid day-of-month for ``year``/``month``.

    Falls back to the last day of February when a 29 February birthday is
    requested in a non-leap year.
    """
    if month == 2 and day == 29:
        # year is a leap year if it divides by 4, except centuries not by 400
        is_leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        return 29 if is_leap else 28
    return day


def make_date(year, month, day):
    """Build a date, resolving a 29 February birthday against ``year``."""
    return date(year, month, _resolve_day(year, month, day))


def next_occurrence(month, day, today=None):
    """Return the next date this month/day occurs on or after ``today``."""
    today = today or date.today()
    candidate = make_date(today.year, month, day)
    if candidate < today:
        candidate = make_date(today.year + 1, month, day)
    return candidate


def days_until_next(month, day, today=None):
    """Number of days until the next occurrence of a birthday."""
    today = today or date.today()
    return (next_occurrence(month, day, today) - today).days


def is_birthday_today(month, day, today=None):
    """True when the birthday falls today (29 Feb maps to 28 Feb off-leap)."""
    today = today or date.today()
    return (today.month, today.day) == (month, _resolve_day(today.year, month, day))


def calculate_age(birth_year, month, day, today=None):
    """Age in whole years, or ``None`` when the birth year is unknown.

    The result is the age the person is *on their next birthday* only when the
    birthday is today; otherwise it is their current age. Callers must not use
    this when ``birth_year`` is falsy.
    """
    if not birth_year:
        return None
    today = today or date.today()
    age = today.year - birth_year
    if (today.month, today.day) < (month, day):
        age -= 1
    return age


def age_turning(birth_year, month, day, today=None):
    """Age the person turns on their next birthday, or ``None`` if unknown."""
    if not birth_year:
        return None
    today = today or date.today()
    upcoming = next_occurrence(month, day, today)
    return upcoming.year - birth_year


def local_today():
    if timezone is not None:
        return timezone.localdate()
    return date.today()

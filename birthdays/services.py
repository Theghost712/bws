"""Birthday calculation service.

All "next birthday" and age wording funnels through here and through
``core.dates`` so the leap-year policy and the unknown-year rule are applied
consistently (see ``core/dates.py`` and ``birthdays/models.py``).
"""

from core.dates import (
    age_turning,
    calculate_age,
    is_birthday_today,
    local_today,
    next_occurrence,
)


def annotate_birthday(birthday, today=None):
    """Return a dict describing the next occurrence of a saved birthday."""
    today = today or local_today()
    month, day = birthday.birthday.month, birthday.birthday.day
    next_date = next_occurrence(month, day, today)
    return {
        "birthday": birthday,
        "next_date": next_date,
        "days_until": (next_date - today).days,
        "is_today": is_birthday_today(month, day, today),
        "age_turning": age_turning(birthday.birth_year, month, day, today),
        "current_age": calculate_age(birthday.birth_year, month, day, today),
    }


def upcoming_birthdays(user, limit=None, within_days=None, today=None):
    """Upcoming birthdays for a user, soonest first."""
    today = today or local_today()
    entries = [annotate_birthday(b, today) for b in user.birthdays.all()]
    entries.sort(key=lambda entry: entry["days_until"])
    if within_days is not None:
        entries = [entry for entry in entries if entry["days_until"] <= within_days]
    if limit is not None:
        entries = entries[:limit]
    return entries


def todays_birthdays(user, today=None):
    today = today or local_today()
    return [b for b in user.birthdays.all() if is_birthday_today(b.birthday.month, b.birthday.day, today)]

from datetime import date
from typing import Optional


def _is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def _resolve_day(year: int, month: int, day: int) -> int:
    if month == 2 and day == 29:
        return 29 if _is_leap_year(year) else 28
    return day


def make_date(year: int, month: int, day: int) -> date:
    return date(year, month, _resolve_day(year, month, day))


def next_occurrence(month: int, day: int, today: Optional[date] = None) -> date:
    today = today or date.today()
    candidate = make_date(today.year, month, day)
    if candidate < today:
        candidate = make_date(today.year + 1, month, day)
    return candidate


def is_birthday_today(month: int, day: int, today: Optional[date] = None) -> bool:
    today = today or date.today()
    return (today.month, today.day) == (month, _resolve_day(today.year, month, day))

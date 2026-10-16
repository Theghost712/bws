from datetime import date

from paveline_bot.core.dates import next_occurrence, make_date, is_birthday_today


def test_leap_year_birthday_maps_to_28_feb():
    assert next_occurrence(2, 29, date(2026, 2, 27)) == date(2026, 2, 28)
    assert next_occurrence(2, 29, date(2024, 2, 1)) == date(2024, 2, 29)


def test_next_occurrence_rolls_to_next_year():
    assert next_occurrence(1, 1, date(2026, 6, 1)) == date(2027, 1, 1)


def test_is_birthday_today():
    assert is_birthday_today(10, 14, date(2026, 10, 14)) is True
    assert is_birthday_today(10, 15, date(2026, 10, 14)) is False

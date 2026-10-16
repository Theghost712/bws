import pytest

from paveline_bot.core.validators import sanitize_extra, validate_wish_output


def test_valid_wish_accepted():
    assert validate_wish_output("Happy birthday, dear friend!") is True


def test_ai_failure_text_rejected():
    assert validate_wish_output("As an AI, I cannot write wishes.") is False


def test_markdown_rejected():
    assert validate_wish_output("**Happy birthday**!") is False


def test_empty_rejected():
    assert validate_wish_output("") is False


def test_sanitize_strips_control_chars():
    assert sanitize_extra("bad\x00text") == "bad text"

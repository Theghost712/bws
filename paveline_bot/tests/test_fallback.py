from paveline_bot.core.fallback_templates import generate_fallback_wish


def test_fallback_generates_wish():
    wish = generate_fallback_wish(name="Alice", relationship="friend", language="en", style="heartfelt")
    assert wish is not None
    assert len(wish) > 0


def test_all_languages_work():
    for lang in ["en", "sw", "fr", "es", "ar"]:
        wish = generate_fallback_wish(name="Test", language=lang)
        assert len(wish) > 0

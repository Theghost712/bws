import pytest

from paveline_bot.core.wish_service import generate_wish, generate_wishes


@pytest.mark.asyncio
async def test_generate_wish_returns_valid_fallback():
    context = {
        "name": "Amina",
        "relationship": "friend",
        "language": "en",
        "style": "heartfelt",
        "sender": "",
        "extra": "",
        "length": "medium",
        "age": None,
    }
    wish = await generate_wish(context, variation=0)
    assert "text" in wish
    assert wish["text"]


@pytest.mark.asyncio
async def test_generate_wishes_returns_three_variants():
    context = {
        "name": "Amina",
        "relationship": "friend",
        "language": "en",
        "style": "heartfelt",
        "sender": "",
        "extra": "",
        "length": "medium",
        "age": None,
    }
    wishes = await generate_wishes(context, count=3)
    assert len(wishes) == 3

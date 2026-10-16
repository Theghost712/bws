import pytest

from paveline_bot.ai.base import FallbackProvider
from paveline_bot.ai.router import AIRouter


class FakeFailingProvider:
    def __init__(self):
        self.calls = 0

    async def generate(self, prompt, system=None):
        self.calls += 1
        raise Exception("simulated AI failure")


@pytest.mark.asyncio
async def test_router_falls_back_when_provider_fails():
    router = AIRouter()
    failing = FakeFailingProvider()
    fallback = FallbackProvider(lambda: "Offline fallback wish")
    router.providers = [failing, fallback]
    text = await router.generate("test prompt", "test system")
    assert text == "Offline fallback wish"
    assert failing.calls >= 1

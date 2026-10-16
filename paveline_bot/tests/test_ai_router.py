from paveline_bot.ai.router import AIRouter


def test_router_exists():
    router = AIRouter()
    assert router is not None

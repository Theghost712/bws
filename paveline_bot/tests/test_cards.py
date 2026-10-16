from paveline_bot.cards.designer import render_card, card_to_bytes


def test_card_rendering():
    image = render_card(heading="Happy Birthday!", message="Have a great day!", signoff="With love")
    assert image is not None
    assert image.size == (1080, 1080)
    data = card_to_bytes(image)
    assert len(data) > 0

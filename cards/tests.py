import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from .models import CardTemplate
from .services import render_card


def make_image_bytes(fmt="PNG", size=(120, 120)):
    buffer = io.BytesIO()
    Image.new("RGB", size, (200, 120, 130)).save(buffer, format=fmt)
    buffer.seek(0)
    return buffer.read()


class GalleryTests(TestCase):
    def test_templates_seeded(self):
        self.assertGreaterEqual(CardTemplate.objects.filter(is_active=True).count(), 8)

    def test_gallery_loads(self):
        response = self.client.get(reverse("cards:gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Birthday card gallery")

    def test_gallery_category_filter(self):
        response = self.client.get(reverse("cards:gallery"), {"category": "romantic"})
        self.assertEqual(response.status_code, 200)


class DesignerTests(TestCase):
    def test_designer_loads(self):
        self.assertEqual(self.client.get(reverse("cards:designer")).status_code, 200)

    def test_render_returns_png(self):
        response = self.client.post(
            reverse("cards:render"),
            {
                "template": "romantic-blush", "language": "en", "recipient_name": "Amina",
                "message": "Have a wonderful birthday!", "sender_name": "Juma",
                "font": "serif", "accent": "#bd685f", "orientation": "landscape", "heading": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        content = b"".join(response.streaming_content)
        self.assertTrue(content.startswith(b"\x89PNG"))

    def test_render_rejects_bad_image(self):
        bad = SimpleUploadedFile("notes.txt", b"not an image", content_type="text/plain")
        response = self.client.post(
            reverse("cards:render"),
            {
                "template": "romantic-blush", "language": "en", "message": "hi",
                "font": "serif", "accent": "#bd685f", "orientation": "landscape", "photo": bad,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_render_accepts_photo(self):
        photo = SimpleUploadedFile("pic.png", make_image_bytes(), content_type="image/png")
        response = self.client.post(
            reverse("cards:render"),
            {
                "template": "elegant-midnight", "language": "en", "recipient_name": "Amina",
                "message": "Happy birthday!", "font": "serif", "accent": "#d9b56a",
                "orientation": "portrait", "photo": photo,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_template_preview(self):
        response = self.client.get(reverse("cards:template_preview", args=["floral-garden"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")


class RenderServiceTests(TestCase):
    def test_render_card_arabic(self):
        template = CardTemplate.objects.get(slug="romantic-blush")
        image = render_card(
            template,
            heading="عيد ميلاد سعيد، أمينة!",
            message="كل عام وأنت بخير.",
            signoff="مع كل الحب",
        )
        self.assertEqual(image.mode, "RGB")

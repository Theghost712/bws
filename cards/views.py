from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from wishes.messages import HELLO

from .forms import CardDesignForm
from .models import CardTemplate
from .services import image_to_bytes, render_card


def gallery(request):
    templates = CardTemplate.objects.filter(is_active=True)
    category = request.GET.get("category", "").strip()
    if category:
        templates = templates.filter(category=category)
    return render(
        request,
        "cards/gallery.html",
        {
            "templates": templates,
            "category": category,
            "categories": CardTemplate._meta.get_field("category").choices,
        },
    )


def designer(request):
    templates = CardTemplate.objects.filter(is_active=True)
    initial = {"accent": templates[0].accent if templates.exists() else "#bd685f"}
    prefill = ("template", "message", "heading", "recipient_name", "sender_name", "language")
    for key in prefill:
        value = request.GET.get(key)
        if value:
            initial[key] = value
    form = CardDesignForm(initial=initial)
    return render(request, "cards/designer.html", {"form": form, "templates": templates})


def _build_card(template, form):
    data = form.cleaned_data
    language = data.get("language", "en")
    recipient = (data.get("recipient_name") or "").strip()
    heading = (data.get("heading") or "").strip()
    if not heading:
        greeting = HELLO.get(language, HELLO["en"])
        heading = f"{greeting}, {recipient}!" if recipient else f"{greeting}!"
    message = (data.get("message") or "").strip() or "Wishing you a day as lovely as you are."
    sender = (data.get("sender_name") or "").strip()
    signoff = f"With love, {sender}" if sender else "With love"
    return render_card(
        template,
        heading=heading,
        message=message,
        signoff=signoff,
        font_name=data.get("font", "serif"),
        accent=data.get("accent"),
        orientation=data.get("orientation"),
        photo=data.get("photo"),
    )


@require_POST
def render_image(request):
    form = CardDesignForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    template = form.cleaned_data["template"]
    image = _build_card(template, form)
    buffer = image_to_bytes(image)
    download = request.POST.get("download") == "1"
    filename = f"paveline-{template.slug}.png"
    response = FileResponse(
        buffer,
        as_attachment=download,
        filename=filename,
        content_type="image/png",
    )
    return response


def template_preview(request, slug):
    template = get_object_or_404(CardTemplate, slug=slug, is_active=True)
    image = render_card(
        template,
        heading="Happy birthday!",
        message=template.description or "Wishing you a beautiful day.",
        signoff="With love",
    )
    return FileResponse(image_to_bytes(image), content_type="image/png")

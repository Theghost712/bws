from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SavedWishForm, WishNoteForm, WishRequestForm
from .models import BirthdayWish, Favorite
from .services import as_share_text, generate_alternatives, generate_wish


def create(request):
    """Render and process the wish request form (works for anonymous users)."""
    if request.method == "POST":
        form = WishRequestForm(request.POST)
        if form.is_valid():
            request.session["wish_context"] = form.generation_context()
            return redirect("wishes:result")
    else:
        initial = {"language": request.LANGUAGE_CODE}
        for key in ("tone", "relationship", "language"):
            value = request.GET.get(key)
            if value:
                initial[key] = value
        name = request.GET.get("name")
        if name:
            initial["name"] = name[:60]
        form = WishRequestForm(initial=initial)
    return render(request, "wishes/create.html", {"form": form})


def _get_context(request):
    context = request.session.get("wish_context")
    if not context:
        return None
    return context


def result(request):
    """Show a generated wish plus alternatives, using a PRG-friendly session."""
    context = _get_context(request)
    if not context:
        messages.info(request, "Add a few details and we will create a wish for you.")
        return redirect("wishes:create")

    try:
        variation = max(0, int(request.GET.get("v", 0)))
    except (TypeError, ValueError):
        variation = 0

    wish = generate_wish(variation=variation, **context)
    alternatives = generate_alternatives(context, count=3)
    return render(
        request,
        "wishes/result.html",
        {
            "wish": wish,
            "alternatives": alternatives,
            "share_text": as_share_text(wish),
            "variation": variation,
            "context": context,
        },
    )


@login_required
@require_POST
def save_wish(request):
    """Persist a wish the user generated. Requires an authenticated owner."""
    form = SavedWishForm(request.POST)
    if form.is_valid():
        wish = form.save(commit=False)
        wish.owner = request.user
        wish.save()
        messages.success(request, "Wish saved to your collection.")
        return redirect("wishes:saved_detail", pk=wish.pk)
    messages.error(request, "We could not save that wish. Please try again.")
    return redirect("wishes:result")


@login_required
def saved_list(request):
    wishes = BirthdayWish.objects.filter(owner=request.user)
    query = request.GET.get("q", "").strip()
    if query:
        wishes = wishes.filter(recipient_name__icontains=query)
    language = request.GET.get("language", "").strip()
    if language:
        wishes = wishes.filter(language=language)
    favorites = Favorite.objects.filter(user=request.user).values_list("wish_id", flat=True)
    return render(
        request,
        "wishes/saved_list.html",
        {
            "wishes": wishes,
            "query": query,
            "language": language,
            "favorite_ids": set(favorites),
        },
    )


@login_required
def saved_detail(request, pk):
    wish = get_object_or_404(BirthdayWish, pk=pk, owner=request.user)
    is_favorite = Favorite.objects.filter(user=request.user, wish=wish).exists()
    return render(
        request,
        "wishes/saved_detail.html",
        {"wish": wish, "is_favorite": is_favorite, "share_text": wish.share_text()},
    )


@login_required
def saved_edit(request, pk):
    wish = get_object_or_404(BirthdayWish, pk=pk, owner=request.user)
    if request.method == "POST":
        form = WishNoteForm(request.POST, instance=wish)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated.")
            return redirect("wishes:saved_detail", pk=wish.pk)
    else:
        form = WishNoteForm(instance=wish)
    return render(request, "wishes/saved_edit.html", {"wish": wish, "form": form})


@login_required
@require_POST
def saved_delete(request, pk):
    wish = get_object_or_404(BirthdayWish, pk=pk, owner=request.user)
    wish.delete()
    messages.success(request, "Wish deleted.")
    return redirect("wishes:saved_list")


@login_required
@require_POST
def toggle_favorite(request, pk):
    wish = get_object_or_404(BirthdayWish, pk=pk, owner=request.user)
    favorite, created = Favorite.objects.get_or_create(user=request.user, wish=wish)
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favourites.")
    else:
        messages.success(request, "Added to favourites.")
    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("wishes:saved_detail", pk=wish.pk)


@login_required
def favorites_list(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("wish")
        .order_by("-created_at")
    )
    return render(request, "wishes/favorites.html", {"favorites": favorites})

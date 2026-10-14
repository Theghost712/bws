from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.dates import local_today

from .forms import BirthdayForm
from .models import Birthday
from .services import annotate_birthday, todays_birthdays, upcoming_birthdays


@login_required
def birthday_list(request):
    birthdays = Birthday.objects.filter(owner=request.user)
    query = request.GET.get("q", "").strip()
    relationship = request.GET.get("relationship", "").strip()
    sort = request.GET.get("sort", "name")

    if query:
        birthdays = birthdays.filter(
            Q(recipient_name__icontains=query) | Q(notes__icontains=query)
        )
    if relationship:
        birthdays = birthdays.filter(relationship=relationship)

    if sort == "recent":
        birthdays = birthdays.order_by("-created_at")
    else:
        birthdays = birthdays.order_by("recipient_name")

    return render(
        request,
        "birthdays/list.html",
        {
            "birthdays": birthdays,
            "query": query,
            "relationship": relationship,
            "sort": sort,
            "relationships": Birthday._meta.get_field("relationship").choices,
        },
    )


@login_required
def birthday_detail(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk, owner=request.user)
    return render(request, "birthdays/detail.html", {"birthday": birthday, "info": annotate_birthday(birthday)})


@login_required
def birthday_add(request):
    if request.method == "POST":
        form = BirthdayForm(request.POST)
        if form.is_valid():
            birthday = form.save(commit=False)
            birthday.owner = request.user
            birthday.save()
            messages.success(request, f"{birthday.recipient_name}'s birthday has been saved.")
            return redirect("birthdays:detail", pk=birthday.pk)
    else:
        form = BirthdayForm()
    return render(request, "birthdays/form.html", {"form": form, "is_edit": False})


@login_required
def birthday_edit(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk, owner=request.user)
    if request.method == "POST":
        form = BirthdayForm(request.POST, instance=birthday)
        if form.is_valid():
            form.save()
            messages.success(request, "Birthday updated.")
            return redirect("birthdays:detail", pk=birthday.pk)
    else:
        form = BirthdayForm(instance=birthday)
    return render(request, "birthdays/form.html", {"form": form, "birthday": birthday, "is_edit": True})


@login_required
@require_POST
def birthday_delete(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk, owner=request.user)
    name = birthday.recipient_name
    birthday.delete()
    messages.success(request, f"{name}'s birthday was deleted.")
    return redirect("birthdays:list")


@login_required
def birthday_upcoming(request):
    today = local_today()
    return render(
        request,
        "birthdays/upcoming.html",
        {
            "upcoming": upcoming_birthdays(request.user, within_days=90),
            "today": todays_birthdays(request.user, today),
            "today_date": today,
        },
    )

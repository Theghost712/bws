from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.dates import local_today

from .forms import ReminderForm
from .models import Reminder
from .services import delivery_date


@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(user=request.user).select_related("birthday")
    today = local_today()
    upcoming = sorted(
        [{"reminder": reminder, "date": delivery_date(reminder, today)} for reminder in reminders],
        key=lambda item: item["date"],
    )
    return render(
        request,
        "reminders/list.html",
        {"reminders": reminders, "upcoming": upcoming, "today": today},
    )


@login_required
def reminder_add(request):
    if not request.user.birthdays.exists():
        messages.info(request, "Save a birthday first, then set a reminder for it.")
        return redirect("birthdays:add")
    if request.method == "POST":
        form = ReminderForm(request.POST, user=request.user)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, "Reminder saved.")
            return redirect("reminders:list")
    else:
        form = ReminderForm(user=request.user)
    return render(request, "reminders/form.html", {"form": form, "is_edit": False})


@login_required
def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=reminder, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Reminder updated.")
            return redirect("reminders:list")
    else:
        form = ReminderForm(instance=reminder, user=request.user)
    return render(request, "reminders/form.html", {"form": form, "reminder": reminder, "is_edit": True})


@login_required
@require_POST
def reminder_toggle(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.is_enabled = not reminder.is_enabled
    reminder.save(update_fields=["is_enabled", "updated_at"])
    state = "enabled" if reminder.is_enabled else "disabled"
    messages.success(request, f"Reminder {state}.")
    return redirect("reminders:list")


@login_required
@require_POST
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, user=request.user)
    reminder.delete()
    messages.success(request, "Reminder deleted.")
    return redirect("reminders:list")

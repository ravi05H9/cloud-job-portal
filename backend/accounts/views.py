from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from jobs.models import Application


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related("job").order_by("-applied_at")
    return render(request, "accounts/my_applications.html", {"applications": applications})

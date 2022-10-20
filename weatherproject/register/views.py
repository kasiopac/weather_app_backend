from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            raise ValueError(form.errors)
        return redirect("/login")
    else:
        form = UserCreationForm()
    return render(request, "register/register.html", {"form": form})


from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # for flash messages
from django.urls import reverse
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group


# Create your views here.


def index(request):
    return render(request, "restr/index.html")


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            owner = Group.objects.get(name="owner")

            user.groups.add(owner)
            user.save()

            messages.success(
                request, "Account created successfully for " + user.username
            )
            return HttpResponseRedirect(reverse("restr:login"))

    context = {"form": form}

    return render(request, "restr/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request, username=username, password=password
        )  # matching username and password of login input field and stored usernames from database that is registered

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("restr:index"))

        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, "restr/login.html")


def logoutUser(request):
    logout(request)
    return render(request, "restr/login.html")

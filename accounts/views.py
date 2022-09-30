from tokenize import Name
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError

from .models import *

def index(request):
    if request.user.is_authenticated:
        message = "You are logged in."
    else:
        message = "This is accounts route and you are a guest."

    return render(request, "accounts/index.html", {
        "message": message,
        "logged_in": request.user.is_authenticated,
        "username": request.user.username,
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home:index"))
        else:
            return render(request, "accounts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "accounts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            if request.POST["position"] == "student":
                new_student = Student(Person=user, is_verified=False, Department=Department.objects.get(Code=request.POST["department"]))
                new_student.save()
            if request.POST["position"] == "teacher":
                new_teacher = Teacher(Person=user, is_verified=False, Department=Department.objects.get(Code=request.POST["department"]))
                new_teacher.save()
        except IntegrityError:
            return render(request, "accounts/register.html", {
                "message": "Something went wrong, please contact support team."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home:index"))
    else:
        return render(request, "accounts/register.html", context={
            "departments": [x for x in Department.objects.all()]
        })

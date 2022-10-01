from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import *


def index(request):
    # For SuperUser Users
    if request.user.is_superuser:
        name = request.user.username.title()
        department = "None"
        account_type = "Superuser"

    # For Authenticated Users
    elif request.user.is_authenticated:
        name = request.user.username.title()
        department = request.user.Department

        if request.user.is_student and request.user.is_verified:
            account_type = "Student (Verified)"

        elif request.user.is_student and not request.user.is_verified:
            account_type = "Student (Pending Verification)"

        elif request.user.is_teacher and request.user.is_verified:
            account_type = "Teacher (Verified)"

        elif request.user.is_teacher and not request.user.is_verified:
            account_type = "Teacher (Pending Verification)"

        else:
            account_type = "Default"

    # For Anonymous Users
    else:
        name = "Guest"
        department = "None"
        account_type = "AnonymousUser"

    return render(request, "home/index.html", {
        "name": name,
        "department": department,
        "account_type": account_type,
    })

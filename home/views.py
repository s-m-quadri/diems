from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import *


def index(request):
    if request.user.is_authenticated:
        if Student.objects.get(Person=request.user):
            account_type = "Student"
            account = Student.objects.get(Person=request.user)
            name = account.Person.username.title()
            pages = Page.objects.filter(Department=account.Department)

        elif Teacher.objects.get(Person=request.user):
            account_type = "Teacher"
            account = Teacher.objects.get(Person=request.user)
            name = account.Person.username.title()
            pages = Page.objects.filter(Department=account.Department)

        else:
            account_type = "Unknown"
            name = "Guest"
            account = None
    else:
        # The user is anonymous
        account_type = "AnonymousUser"
        name = "Guest"
        account = None
        pages = None
        

    return render(request, "home/index.html", {
        "account_type": account_type,
        "account": account,
        "name": name,
        "pages": pages,
    })

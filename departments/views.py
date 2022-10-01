from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from .models import *
from accounts.models import *


def index(request, code):
    try:
        department = Department.objects.get(Code=code)
        return render(request, "departments/index.html", {
            "title": f"Welcome to {department.Name}",
            "pages": [x for x in Page.objects.filter(Department=department)]
        })
    except ObjectDoesNotExist:
        return render(request, "departments/index.html", {
            "title": f"Page not found",
        })

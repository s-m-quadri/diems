from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from accounts.models import *


class AddDepartmentForm(forms.Form):
    Name = forms.CharField(
        label="Name", max_length=64, min_length=1, strip=True, required=True)
    Code = forms.CharField(
        label="Code (unique)", max_length=16, min_length=1, strip=True, required=True)


class AddPageForm(forms.Form):
    Name = forms.CharField(
        label="Name", max_length=64, min_length=1, strip=True, required=True)
    Code = forms.CharField(
        label="Code (unique)", max_length=32, min_length=1, strip=True, required=True)



def index(request, code):
    try:
        department = Department.objects.get(Code=code)
        return render(request, "departments/index.html", {
            "title": f"Welcome to {department.Name} Department",
            "pages": [x for x in Page.objects.filter(Department=department)],
            "code": code,
        })
    except ObjectDoesNotExist:
        return render(request, "departments/index.html", {
            "title": f"Page not found",
        })


def list_department(request):
    return render(request, "departments/list.html", {
        "title": "Department Activity Management",
        "departments": [x for x in Department.objects.all()]
    })


def add_department(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home:index")) 

    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render(request, "home/form_page.html", {
            "title": "Create Department",
            "to": reverse("departments:add_department"),
            "action": "Create it",
            "form": AddDepartmentForm(),
        })

    # Ensure fields are valid
    form = AddDepartmentForm(request.POST)
    if not form.is_valid():
        return render(request, "home/form_page.html", {
            "title": "Create Department",
            "to": reverse("departments:add_department"),
            "action": "Create it",
            "message": "Form is not valid, make necessary changes",
            "form": AddDepartmentForm(request.POST),
        })
    data = form.cleaned_data

    # Attempt to create new department
    try:
        # Collect Requirements
        department_name = data["Name"].title()
        department_code = data["Code"].lower()

        # Make space for the new department
        new_department = Department(Name=department_name, Code=department_code)
        new_department.save()
        new_page = Page(Name="Admin", Code=f"{department_code}-admin",
                            Department=new_department)
        new_page.save()

    except Exception as massage:
        return render(request, "home/form_page.html", {
            "title": "Create Department",
            "to": reverse("departments:add_department"),
            "action": "Create it",
            "message": "Something went wrong, please contact support team regarding exception '{}'".format(massage),
            "form": AddDepartmentForm(request.POST),
        })

    # Redirect to the department page
    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": department_code}))


def add_page(request, code):

    if not request.user.is_teacher:
        return HttpResponseRedirect(reverse("departments:index", kwargs={"code": code})) 

    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render(request, "home/form_page.html", {
            "title": "Create Page",
            "to": reverse("departments:add_page", kwargs={"code": code}),
            "action": "Create it",
            "form": AddPageForm(),
        })

    # Ensure fields are valid
    form = AddPageForm(request.POST)
    if not form.is_valid():
        return render(request, "home/form_page.html", {
            "title": "Create Page",
            "to": reverse("departments:add_page", kwargs={"code": code}),
            "action": "Create it",
            "message": "Form is not valid, make necessary changes",
            "form": AddPageForm(request.POST),
        })
    data = form.cleaned_data

    # Attempt to create new page
    try:
        # Collect Requirements
        if request.user.is_teacher:
            page_name = data["Name"].title()
            page_code = f'{request.user.Department.Code}-{data["Code"].lower()}'
            page_department = request.user.Department
            new_page = Page(Name=page_name, Code=page_code,
                            Department=page_department)
            new_page.save()

    except Exception as massage:
        return render(request, "home/form_page.html", {
            "title": "Create Page",
            "to": reverse("departments:add_page", kwargs={"code": code}),
            "action": "Create it",
            "message": "Something went wrong, please contact support team regarding exception '{}'".format(massage),
            "form": AddPageForm(request.POST),
        })

    # Redirect to the department page
    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": code}))

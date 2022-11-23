from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from home.views import render_form_generic
from accounts.models import *
from codeshine.models import Assignment


def index(request, code):
    try:
        department = Department.objects.get(Code=code)
        pages = Page.objects.filter(Department=department)
        assignments = []
        for page in pages:
            assignments += [x for x in Assignment.objects.filter(In=page).order_by("-pk")]
        return render(request, "departments/index.html", {
            "title": f"Welcome to {department.Name} Department",
            "pages": [x for x in pages],
            "assignments": assignments,
            "code": code,
        })
    except ObjectDoesNotExist:
        return render(request, "departments/index.html", {
            "title": f"Page not found",
        })


def list_department(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home:index"))
    
    return render(request, "departments/list.html", {
        "title": "Department Activity Management",
        "departments": [x for x in Department.objects.all()]
    })


def add_department(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home:index"))

    class AddDepartmentForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=16, min_length=1, strip=True, required=True)

    form_title = "Create Department"
    form_to = reverse("departments:add_department")
    form_action = "Create it"

    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, AddDepartmentForm())

    raw_form = AddDepartmentForm(request.POST)
    if not raw_form.is_valid():
        return render_form_generic(
            request, form_title, form_to, form_action,
            AddDepartmentForm(request.POST),
            error="Form is not valid, make necessary changes")

    try:
        form_data = raw_form.cleaned_data

        department_name = form_data["Name"].title()
        department_code = form_data["Code"].lower()
        new_department = Department(Name=department_name, Code=department_code)
        new_department.save()

        new_page = Page(Name="Admin",
                        Code=f"{department_code}-admin",
                        Department=new_department)
        new_page.save()

    except Exception as massage:
        return render_form_generic(
            request, form_title, form_to, form_action,
            AddDepartmentForm(request.POST),
            error="Something went wrong, please contact support team regarding exception '{}'".format(massage))

    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": department_code}))


def add_page(request, code):
    class AddPageForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=32, min_length=1, strip=True, required=True)

    form_title = "Create Page"
    form_to = reverse("departments:add_page", kwargs={"code": code})
    form_action = "Create it"

    if not request.user.is_teacher:
        return HttpResponseRedirect(reverse("departments:index", kwargs={"code": code}))

    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, AddPageForm())

    raw_form = AddPageForm(request.POST)
    if not raw_form.is_valid():
        return render_form_generic(
            request, form_title, form_to, form_action,
            AddPageForm(request.POST),
            error="Form is not valid, make necessary changes")

    try:
        form_data = raw_form.cleaned_data
        if request.user.is_teacher:
            new_page = Page(
                Name=form_data["Name"].title(),
                Code=f'{request.user.Department.Code}-{form_data["Code"].lower()}',
                Department=request.user.Department)
            new_page.save()

    except Exception as massage:
        return render_form_generic(
            request, form_title, form_to, form_action, AddPageForm(
                request.POST),
            error="Something went wrong, please contact support team regarding exception '{}'".format(massage))

    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": code}))

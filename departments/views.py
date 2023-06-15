from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from home.views import render_form_generic
from accounts.models import *
from codeshine.models import Assignment


def specific_department(request, code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    department = get_object_or_404(Department, Code=code)

    # Ensure user is in same department
    if not request.user.Department == department:
        return render(request, "home/403.html", status=403)

    class AddPageForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=32, min_length=1, strip=True, required=True)

    assignments = []
    pages = get_list_or_404(Page, Department=department)
    for page in pages:
        assignments += [x for x in Assignment.objects.filter(
            In=page).order_by("-pk")]

    return render(request, "departments/index.html", {
        "title": f"{department.Name} Department",
        "pages": [x for x in pages],
        "assignments": assignments,
        "code": code,
        "form": AddPageForm()
    })


def all_departments(request):
    # Ensure the user is super user
    if not request.user.is_superuser:
        return render(request, "home/403.html", status=403)

    class AddDepartmentForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=16, min_length=1, strip=True, required=True)

    return render(request, "departments/list.html", {
        "title": "Department Activity Management",
        "departments": [x for x in Department.objects.all()],
        "form": AddDepartmentForm(),
    })


def add_department(request):
    # Ensure the user is superuser
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("home:index"))

    class AddDepartmentForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=16, min_length=1, strip=True, required=True)

    return_url = reverse("departments:all_departments")

    if not request.method == "POST":
        return HttpResponseRedirect(return_url)

    raw_form = AddDepartmentForm(request.POST)
    if not raw_form.is_valid():
        return render(request, "home/400.html", context={
            "return_url": return_url,
            "backup_data": AddDepartmentForm(request.POST)
        })

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

    except Exception as exception:
        return render(request, "home/400.html", context={
            "exception": exception,
            "return_url": return_url,
            "backup_data": AddDepartmentForm(request.POST)
        })

    return HttpResponseRedirect(return_url)


def add_page(request, code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    # Ensure user is in same department
    if not request.user.Department.Code == code:
        return render(request, "home/403.html", status=403)

    # Ensure user is teacher
    if not request.user.is_teacher:
        return render(request, "home/403.html", status=403)

    return_url = reverse("departments:specific_department", kwargs={
        "code": code
    })

    class AddPageForm(forms.Form):
        Name = forms.CharField(
            label="Name", max_length=64, min_length=1, strip=True, required=True)
        Code = forms.CharField(
            label="Code (unique)", max_length=32, min_length=1, strip=True, required=True)

    if not request.method == "POST":
        return HttpResponseRedirect(return_url)

    raw_form = AddPageForm(request.POST)
    if not raw_form.is_valid():
        return render(request, "home/400.html", context={
            "return_url": return_url,
            "backup_data": AddPageForm(request.POST)
        })

    try:
        form_data = raw_form.cleaned_data
        if request.user.is_teacher:
            new_page = Page(
                Name=form_data["Name"].title(),
                Code=f'{request.user.Department.Code}-{form_data["Code"].lower()}',
                Department=request.user.Department)
            new_page.save()

    except Exception as exception:
        return render(request, "home/400.html", context={
            "exception": exception,
            "return_url": return_url,
            "backup_data": AddPageForm(request.POST)
        })

    return HttpResponseRedirect(return_url)

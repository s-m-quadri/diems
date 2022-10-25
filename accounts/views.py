from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.mail import send_mail


from .models import Department, User


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", max_length=100, min_length=1, strip=True, required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(), required=True)


class RegistrationForm(forms.Form):
    PositionChoices = [("student", "As a Student"),
                       ("teacher", "As a Teacher")]

    username = forms.CharField(
        label="Username", max_length=100, min_length=1, strip=True, required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(), required=True)
    confirmation = forms.CharField(
        label="Retype Password", widget=forms.PasswordInput(), required=True)
    email = forms.CharField(
        label="Email", max_length=100, min_length=1, strip=True, required=True)
    position = forms.ChoiceField(
        label="Position", choices=PositionChoices, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="None", required=True)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("accounts:login"))


def login_view(request):
    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render(request, "home/form_page.html", {
            "title": "Login",
            "to": reverse("accounts:login"),
            "action": "Authenticate me",
            "form": LoginForm,
        })

    # Ensure fields are valid
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, "home/form_page.html", {
            "title": "Login",
            "to": reverse("accounts:login"),
            "action": "Now, Authenticate me",
            "message": "Form is not valid, make necessary changes",
            "form": LoginForm(request.POST),
        })
    data = form.cleaned_data

    # Check if authentication successful
    username = data["username"]
    password = data["password"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, "home/form_page.html", {
            "title": "Login",
            "to": reverse("accounts:login"),
            "action": "Now, Authenticate me",
            "message": "Invalid username and/or password",
            "form": LoginForm(request.POST),
        })

    # Log the user in
    login(request, user)
    # email = request.user.email
    # send_mail(
    #     subject='Subject here',
    #     message='Here is the message.',
    #     from_email='webmaster@localhost',
    #     recipient_list=[email],
    #     fail_silently=False
    # )
    return HttpResponseRedirect(reverse("home:index"))


def logout_view(request):
    # Log the user out
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))


def register_view(request):
    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render(request, "home/form_page.html", {
            "title": "Register",
            "to": reverse("accounts:register"),
            "action": "Register me",
            "form": RegistrationForm(),
        })

    # Ensure fields are valid
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, "home/form_page.html", {
            "title": "Register",
            "to": reverse("accounts:register"),
            "action": "Register me",
            "message": "Form is not valid, make necessary changes",
            "form": RegistrationForm(request.POST),
        })
    data = form.cleaned_data

    # Ensure password matches confirmation
    if data["password"] != data["confirmation"]:
        return render(request, "home/form_page.html", {
            "title": "Register",
            "to": reverse("accounts:register"),
            "action": "Register me",
            "message": "Passwords must match.",
            "form": RegistrationForm(request.POST),
        })

    # Attempt to create new user
    try:
        # Collect Requirements
        username = data["username"]
        email = data["email"].lower()
        password = data["password"]

        # Make space for the user
        user = User.objects.create_user(username, email, password)
        user.Department = data["department"]
        user.is_student = True if data["position"] == "student" else False
        user.is_teacher = True if data["position"] == "teacher" else False
        user.save()

    except Exception as massage:
        return render(request, "home/form_page.html", {
            "title": "Register",
            "to": reverse("accounts:register"),
            "action": "Register me",
            "message": "Something went wrong, please contact support team regarding exception '{}'".format(massage),
            "form": RegistrationForm(request.POST),
        })

    # Log the user in
    login(request, user)
    return HttpResponseRedirect(reverse("home:index"))

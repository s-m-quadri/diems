from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


from .models import Department, User
from home.views import render_form_generic


def account_index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("accounts:login"))


def login_view(request):
    class LoginForm(forms.Form):
        username = forms.CharField(
            label="Username", max_length=100, min_length=1, strip=True, required=True)
        password = forms.CharField(
            label="Password", widget=forms.PasswordInput(), required=True)

    form_title = "Login"
    form_to = reverse("accounts:login")
    form_action = "Authenticate me"

    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, LoginForm())

    # Ensure fields are valid
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render_form_generic(request, form_title, form_to, form_action,
                                   LoginForm(request.POST),
                                   error="Form is not valid, make necessary changes")

    data = form.cleaned_data

    # Check if authentication successful
    username = data["username"]
    password = data["password"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render_form_generic(request, form_title, form_to, form_action,
                                   LoginForm(request.POST),
                                   error="Invalid username and/or password")

    # Log the user in
    login(request, user)
    return HttpResponseRedirect(reverse("home:index"))


def logout_view(request):
    # Log the user out
    logout(request)
    return HttpResponseRedirect(reverse("home:index"))


def register_view(request):
    class RegistrationForm(forms.Form):
        PositionChoices = [("student", "As a Student"),
                           ("teacher", "As a Teacher")]

        username = forms.CharField(
            label="Username", max_length=100, min_length=1, strip=True, required=True)
        password = forms.CharField(
            label="Password", widget=forms.PasswordInput(), required=True)
        confirmation = forms.CharField(
            label="Retype Password", widget=forms.PasswordInput(), required=True)
        email = forms.EmailField(
            label="Email", max_length=100, min_length=1, required=True)
        position = forms.ChoiceField(
            label="Position", choices=PositionChoices, required=True)
        department = forms.ModelChoiceField(
            queryset=Department.objects.all(), empty_label="None", required=True)

    form_title = "Register"
    form_to = reverse("accounts:register")
    form_action = "Register me"

    # If user don't POST data, provide the form
    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, RegistrationForm())

    # Ensure fields are valid
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render_form_generic(request, form_title, form_to, form_action,
                                   RegistrationForm(request.POST),
                                   error="Form is not valid, make necessary changes")

    data = form.cleaned_data
    # Ensure password matches confirmation
    if data["password"] != data["confirmation"]:
        return render_form_generic(request, form_title, form_to, form_action,
                                   RegistrationForm(request.POST),
                                   error="Passwords must match")

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
        return render_form_generic(request, form_title, form_to, form_action,
                                   RegistrationForm(request.POST),
                                   error="Something went wrong, please contact support team regarding exception '{}'".format(massage))

    # Log the user in
    login(request, user)
    return HttpResponseRedirect(reverse("home:index"))

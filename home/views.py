from django.shortcuts import render

# from accounts.models import *


def index(request):
    return render(request, "home/index.html")

def render_form_generic(request, title, to, action, form, message=None):
    return render(request, "home/form_page.html", {
        "title": title,
        "to": to,
        "action": action,
        "message": message,
        "form": form,
    })
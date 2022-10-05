from django.shortcuts import render

# from accounts.models import *


def index(request):
    return render(request, "home/index.html")

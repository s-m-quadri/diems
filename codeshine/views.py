from django.shortcuts import render

from .models import *

def index(request, code):
    return render(request, "codeshine/index.html", {
        "massage": "This is codeshine route",
    })
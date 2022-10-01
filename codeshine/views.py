from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def index(request):
    return render(request, "codeshine/index.html", {
        "massage": "This is codeshine route",
    })
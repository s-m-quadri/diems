from django.shortcuts import render

def index(request):
    return render(request, "accounts/index.html", {
        "massage": "This is accounts route",
    })
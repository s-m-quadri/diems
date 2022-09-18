from django.shortcuts import render

def index(request):
    return render(request, "codeshine/index.html", {
        "massage": "This is codeshine route",
    })
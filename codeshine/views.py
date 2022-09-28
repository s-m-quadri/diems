from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def index(request):
    # pages = Page.objects.filter(Department=request.user)

    if request.user in [x.Person for x in list(Student.objects.all())]:
        massage = "log in as student"

    if request.user in [x.Person for x in list(Teacher.objects.all())]:
        massage = "log in as teacher"

    return render(request, "codeshine/index.html", {
        "massage": f"This is codeshine route - {massage}",
        "pages" : Page.objects.all(),
    })
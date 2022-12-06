from django.shortcuts import render


def index(request):
    return render(request, "home/index.html")

def Handler404(request, *args, **kwargs):
    return render(request, "home/404.html", status=404)

def render_form_generic(request, title, to, action, form, message=None, warning=None, error=None):
    return render(request, "home/form_page.html", {
        "title": title,
        "to": to,
        "action": action,
        "form": form,
        "message": message,
        "warning": warning,
        "error": error,
    })

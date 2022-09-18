from django.urls import path

from . import views

app_name = "codeshine"

urlpatterns = [
    path('', views.index, name="index"),
]

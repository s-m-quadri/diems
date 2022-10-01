from django.urls import path

from . import views

app_name = "departments"

urlpatterns = [
    path('<str:code>', views.index, name="index"),
]

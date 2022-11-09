from django.urls import path

from . import views

app_name = "codeshine"

urlpatterns = [
    path('<str:code>-codeshine/', views.index, name="index"),
    path('<str:code>-codeshine/post/', views.index, name="post"),
]

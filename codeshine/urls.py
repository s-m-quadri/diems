from django.urls import path

from . import views

app_name = "codeshine"

urlpatterns = [
    path('<str:page_code>/', views.index, name="index"),
    path('<str:page_code>/post/', views.post_assignment, name="post"),
    path('<str:page_code>/<str:assignment_code>/', views.assignment_index, name="assignment_index"),
    path('<str:page_code>/<str:assignment_code>/submit', views.post_submission, name="submit"),
]

from django.urls import path

from . import views

app_name = "codeshine"

urlpatterns = [
    path('<str:page_code>/', views.index, name="index"),
    path('<str:page_code>/post/', views.post_assignment, name="post"),
    path('<str:page_code>/assignment-<str:assignment_code>/', views.assignment_index, name="assignments"),
    path('<str:page_code>/assignment-<str:assignment_code>/submit/', views.post_submission, name="submit"),
    path('<str:page_code>/assignment-<str:assignment_code>/submissions/', views.submissions, name="submissions"),
    path('<str:page_code>/assignment-<str:assignment_code>/submission-<str:submission_code>/', views.submission_index, name="submission"),
    path('<str:page_code>/assignment-<str:assignment_code>/submission-<str:submission_code>/evaluate', views.post_evaluation, name="evaluate"),
]

from django.urls import path

from . import views
from home.views import Handler404

app_name = "codeshine"

urlpatterns = [
    path('<str:page_code>/post/', views.post_assignment, name="post"),
    path('<str:page_code>/assignment-<str:assignment_code>/', views.specific_assignment, name="assignments"),
    path('<str:page_code>/assignment-<str:assignment_code>/submit/', views.post_submission, name="submit"),
    path('<str:page_code>/assignment-<str:assignment_code>/submissions/', views.submissions, name="submissions"),
    path('<str:page_code>/assignment-<str:assignment_code>/submission-<str:submission_code>/', views.specific_submission, name="submission"),
    path('<str:page_code>/assignment-<str:assignment_code>/submission-<str:submission_code>/evaluate', views.post_evaluation, name="evaluate"),
    path('<str:page_code>/assignment-<str:assignment_code>/submission-<str:submission_code>/comment', views.post_comment, name="comment"),
]
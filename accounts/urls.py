from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.account_index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register")
]

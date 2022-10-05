from django.urls import path

from . import views

app_name = "departments"

urlpatterns = [
    path('departments/', views.list_department, name="list_department"),
    path('departments/add', views.add_department, name="add_department"),
    path('<str:code>-department/add-page', views.add_page, name="add_page"),
    path('<str:code>-department/', views.index, name="index"),
]

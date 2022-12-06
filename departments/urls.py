from django.urls import path, include

from . import views

app_name = "departments"

urlpatterns = [
    path('', views.all_departments, name="all_departments"),
    path('add/', views.add_department, name="add_department"),
    path('<str:code>-department/', views.specific_department, name="specific_department"),
    path('<str:code>-department/add-page/', views.add_page, name="add_page"),
]

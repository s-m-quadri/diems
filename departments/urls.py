from django.urls import path, include

from . import views

app_name = "departments"

urlpatterns = [
    path('all/', views.list_department, name="list_department"),
    path('<str:code>/', views.index, name="index"),
    path('<str:code>/add-new-page/', views.add_page, name="add_page"),
    path('add-new-department/', views.add_department, name="add_department"),
]

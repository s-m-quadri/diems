from django.contrib import admin

from .models import *

admin.site.register(Persons)
admin.site.register(Courses)
admin.site.register(Departments)
from django.contrib import admin

from .models import *

admin.site.register(Institution)
admin.site.register(Department)
admin.site.register(Page)
admin.site.register(Teacher)
admin.site.register(Student)
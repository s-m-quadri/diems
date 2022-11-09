from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = "DIEMS Accounts"


class Users_table(admin.ModelAdmin):
    list_display = ('username', 'email', 'Department',
                    'is_student', 'is_teacher', 'is_verified')


admin.site.register(User, Users_table)

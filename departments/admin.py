from django.contrib import admin

from .models import Department, Page

admin.site.site_header = "DIEMS Departments"


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', 'is_verified')


class PageAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', 'Department', 'is_verified')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Page, PageAdmin)

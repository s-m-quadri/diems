from django.contrib import admin

from .models import Assignment, Submission, Comment

admin.site.site_header = "DIEMS CodeShine"


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('By', 'In', 'On',
                    'Title', 'max_points', 'is_verified')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('By', 'In', 'On',
                    'Points', 'is_ideal', 'is_verified')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('By', 'In', 'On',
                    'Theme', 'is_ideal', 'is_verified')


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Comment, CommentAdmin)

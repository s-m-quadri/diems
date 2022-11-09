from email.policy import default
from django.db import models

from accounts.models import User
from departments.models import Page


class Assignment(models.Model):
    By = models.ForeignKey(to=User, on_delete=models.CASCADE,
                           related_name="Assigned_By", blank=True, null=True)
    In = models.ForeignKey(to=Page, on_delete=models.CASCADE,
                           related_name="Assigned_In", blank=True, null=True)
    On = models.DateField(auto_now=True)

    Title = models.CharField(max_length=128, blank=False, default="Untitled")
    Description = models.CharField(max_length=1024, blank=True)
    Instructions = models.TextField(blank=True)
    GettingStarted_Template = models.TextField(blank=True)
    max_points = models.IntegerField(blank=False, default=100)
    passing_points = models.IntegerField(blank=False, default=35)

    is_verified = models.BooleanField(blank=False, default=False)
    is_archive = models.BooleanField(blank=False, default=False)
    open_for_submission = models.BooleanField(blank=False, default=False)
    open_for_comment = models.BooleanField(blank=False, default=False)

    display_all_result = models.BooleanField(blank=False, default=False)
    display_verified_result = models.BooleanField(blank=False, default=False)
    display_ideal_result = models.BooleanField(blank=False, default=False)
    
    def __str__(self) -> str:
        return f"{self.On}: {self.Title}"


class Submission(models.Model):
    By = models.ForeignKey(to=User, on_delete=models.CASCADE,
                           related_name="Submitter", blank=True, null=True)
    In = models.ForeignKey(to=Assignment, on_delete=models.CASCADE,
                           related_name="Submitted", blank=True, null=True)
    On = models.DateField(auto_now=True)

    Assignment = models.TextField(blank=True)
    Points = models.IntegerField(blank=False, default=0)
    Remark = models.CharField(max_length=1024, blank=True)

    is_verified = models.BooleanField(blank=False, default=False)
    is_ideal = models.BooleanField(blank=False, default=False)
    
    def __str__(self) -> str:
        return f"{self.On}: {self.By}"


class Comment(models.Model):
    By = models.ForeignKey(to=User, on_delete=models.CASCADE,
                           related_name="Commenter", blank=True, null=True)
    In = models.ForeignKey(to=Submission, on_delete=models.CASCADE,
                           related_name="Commented", blank=True, null=True)
    On = models.DateField(auto_now=True)

    Theme = models.CharField(max_length=128, blank=True)
    Comment = models.TextField(blank=True)

    is_verified = models.BooleanField(blank=False, default=False)
    is_ideal = models.BooleanField(blank=False, default=False)

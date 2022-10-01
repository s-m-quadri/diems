from django.db import models

"""
INSTITUTION
    1. Responsible for Departments

DEPARTMENTS
    1. Responsible for Pages
    2. Responsible for Teachers
    3. Responsible for Students
"""


class Institution(models.Model):
    Name = models.CharField(max_length=64)
    Code = models.CharField(max_length=8, unique=True)
    Description = models.CharField(max_length=512, blank=True)

    def __str__(self) -> str:
        return f"{self.Name}"

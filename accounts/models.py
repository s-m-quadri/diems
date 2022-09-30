from django.db import models
from django.contrib.auth.models import User

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
    Description = models.CharField(max_length=512)
    Admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.Name}"


class Department(models.Model):
    Name = models.CharField(max_length=64)
    Code = models.CharField(max_length=8, unique=True)
    Institute = models.ForeignKey(to=Institution, on_delete=models.CASCADE)
    Head = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Name}"


class Page(models.Model):
    Name = models.CharField(max_length=64)
    Department = models.ManyToManyField(
        to=Department, related_name="Offered_Course")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Name}"


class Teacher(models.Model):
    Person = models.OneToOneField(User, on_delete=models.CASCADE)
    Department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, related_name="Mentor")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Person.username}"


class Student(models.Model):
    Person = models.OneToOneField(User, on_delete=models.CASCADE)
    Department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, related_name="Student")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Person.username}"

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
        return f"{self.Name} (managed by {self.Admin})"


class Department(models.Model):
    Name = models.CharField(max_length=64)
    Institute = models.ForeignKey(to=Institution, on_delete=models.CASCADE)
    Head = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Name} (managed by {self.Head}) - under {self.Institute}"


class Page(models.Model):
    Name = models.CharField(max_length=64)
    Department = models.ManyToManyField(
        to=Department, related_name="Offered_Course")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} by ... {}".format(self.Name, ", ".join([x.__str__() for x in self.Department.all()]))


class Teacher(models.Model):
    Person = models.OneToOneField(User, on_delete=models.CASCADE)
    Department = models.ManyToManyField(to=Department, related_name="Mentor")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Person.username} - under {self.Department}"


class Student(models.Model):
    Person = models.OneToOneField(User, on_delete=models.CASCADE)
    Department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, related_name="Student")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Person.username} - under {self.Department}"

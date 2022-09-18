from django.db import models


class Persons(models.Model):
    Name = models.CharField(max_length=64)
    Email = models.EmailField(max_length=64, unique=True)
    Phone_Number = models.CharField(max_length=16)
    Password = models.CharField(max_length=256)
    Last_Login = models.DateTimeField(auto_now=True)


class Courses(models.Model):
    Name = models.CharField(max_length=64)
    Duration = models.IntegerField()
    Teachers = models.ManyToManyField(
        to=Persons, related_name="Mentor_of_course", blank=True)
    Students = models.ManyToManyField(
        to=Persons, related_name="Enroll_in_course", blank=True)


class Departments(models.Model):
    Name = models.CharField(max_length=64)
    Head = models.ForeignKey(
        to=Persons, on_delete=models.CASCADE, related_name="Under_Department")
    Courses = models.ManyToManyField(
        to=Courses, related_name="Under_Department", blank=True)

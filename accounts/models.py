from django.db import models
from django.contrib.auth.models import AbstractUser

from departments.models import Department

class User(AbstractUser):
    Department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, related_name="Mentor", blank=True, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
from django.db import models

from home.models import Institution


class Department(models.Model):
    Name = models.CharField(max_length=64)
    Code = models.CharField(max_length=8, unique=True)
    Institute = models.ForeignKey(to=Institution, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Name}"


class Page(models.Model):
    Name = models.CharField(max_length=64)
    Code = models.CharField(max_length=8, unique=True)
    Department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, related_name="Offered_Course")
    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.Name}"

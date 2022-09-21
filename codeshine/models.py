from django.db import models

from accounts.models import *

class Assignments(models.Model):
    Title = models.CharField(max_length=64)
    Description = models.CharField(max_length=512)
    Attachments = models.FileField(upload_to="Assignments")
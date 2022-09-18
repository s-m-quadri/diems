from django.db import models

class Assignments(models.Model):
    Title = models.CharField(max_length=64)
    Description = models.CharField(max_length=512)
    Attachments = models.FileField(upload_to="Assignments")
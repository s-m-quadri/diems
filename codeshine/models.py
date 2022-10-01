from django.db import models

from accounts.models import *

class Assignment(models.Model):
    pass
#     Title = models.CharField(max_length=64)
#     Description = models.CharField(max_length=512)
#     By = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, related_name="agn_post")
#     To = models.ForeignKey(to=Page, on_delete=models.CASCADE, related_name="agn_post")
#     Attachments = models.FileField(upload_to="Assignments", blank=True)

#     def __str__(self) -> str:
#         return f"[{self.To}] {self.Title} ~by {self.By}"
# models.py
from django.db import models

class EmployeeSignature(models.Model):
    employee_name = models.CharField(max_length=100)
    signature_image_url = models.URLField()

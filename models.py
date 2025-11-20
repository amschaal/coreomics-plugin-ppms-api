from django.db import models
from dnaorder.models import PI

class PPMSGroup(models.Model):
    ppms_id = models.BigIntegerField(null=True)
    imported = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=75, unique=True, primary_key=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    department = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    meta = models.JSONField(default=dict) # store addional data such as import data
    pi = models.OneToOneField(PI, null=True, on_delete=models.CASCADE)


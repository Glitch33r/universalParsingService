from django.db import models


# Create your models here.

class data(models.Model):
    text = models.CharField(max_length=1024)

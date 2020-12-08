from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class data(models.Model):
    text = models.CharField(max_length=1024)


class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    createdAt = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['nickname', 'createdAt'])
        ]


class UnitCode(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    code = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modifiedAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=32)
    text = models.TextField()
    createdAt = models.DateField(auto_now_add=True, blank=True, null=True)


class UnitData(models.Model):
    data = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(
        Unit,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)

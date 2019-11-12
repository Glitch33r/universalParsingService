from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask
import datetime


# Create your models here.

class Profile(models.Model):
    ACC_TYPE_CHOICES = (
        (0, 'Trial'),
        (1, 'Full'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=32, blank=True)
    # avatar = models.ImageField(upload_to='', blank=True)
    api_key = models.CharField(max_length=128, blank=True)
    tasks = models.ManyToManyField(PeriodicTask)
    acc_type = models.CharField(max_length=1, choices=ACC_TYPE_CHOICES, default=ACC_TYPE_CHOICES[0][0])
    expired_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=7))


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

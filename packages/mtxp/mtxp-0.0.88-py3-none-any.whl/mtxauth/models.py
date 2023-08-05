from __future__ import unicode_literals
import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone

from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model

 

# User = get_user_model()

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())

# 使用下面的信号，有问题，因为loaddata的时候创建用户时，也会触发信号。
# @receiver(signals.post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(signals.post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
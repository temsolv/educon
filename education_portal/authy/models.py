import os

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

from classroom.models import Course
from learningcontrol.models import AssignedCourses

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, null=True, blank=True)
    assigned_courses = models.ManyToManyField(AssignedCourses)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='user')


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User
from django.utils.crypto import get_random_string

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.user_profile.save()
    else:
        email = get_random_string(length = 20, allowed_chars = 'abcdefghijklmnopqrstuvwxyz0\
        123456789') + '@gmail.com'
        password = 'qqwert123456'
        user1 = User.object.create(email = email, password = password)
        UserProfile.objects.create(user=user1)
        user1.user_profile.save()
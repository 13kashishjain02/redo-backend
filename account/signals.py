from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Unique,Profile


user = get_user_model()



# unique signal

@receiver(post_save, sender=user)
def create_uuid(sender, instance, created, **kwargs):
    if created:
        Unique.objects.create(user=instance)


@receiver(post_save, sender=user)
def save_uuid(sender, instance, **kwargs):
    instance.unique.save()





# profile signal

@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=user)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
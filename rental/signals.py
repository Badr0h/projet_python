from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile whenever a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile whenever the User is saved.
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # In case the profile wasn't created, create it
        UserProfile.objects.create(user=instance)

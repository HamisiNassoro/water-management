import logging

###signal sent once model has been saved
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import Profile,Customer
from water_management.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=AUTH_USER_MODEL)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()
    logger.info(f"{instance}'s customer created")
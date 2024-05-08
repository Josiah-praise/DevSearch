from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.models import Socials


@receiver(post_save, sender=get_user_model())
def create_socials(sender, instance, **kwargs):
    '''
    creates a record for a specific user
    in the socials table
    '''
    pass

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from musics.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender,  **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
        print(f'Profile is created for this user: {kwargs["instance"]}')

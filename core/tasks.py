import datetime
from celery import shared_task
from .models import User
from django.utils import timezone


@shared_task
def delete_unactive_users():
    unactive_users = User.objects.filter(is_active=False)\
        .filter(date_joined__lt=timezone.now() - datetime.timedelta(hours=1))
    unactive_users.delete()

    print('All unactive users successfully removed!!!.')
    return True

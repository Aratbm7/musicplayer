from django.db import models
from .validators import image_size, music_size, music_type
from django.conf import settings

class Profile(models.Model):
    Artist = 'a'
    CUSTOMER =  'c'
    USER_MODE = [
        (Artist, 'artist'),
        (CUSTOMER, 'customer')
    ]

    image = models.ImageField(upload_to='media/profie-images', validators=[image_size])
    user_mode = models.CharField(max_length=1, choices=USER_MODE, default=CUSTOMER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='profile')

class Album(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Song(models.Model):
    music_file = models.FileField(upload_to='media/songs', validators=[music_type, music_size])
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, models.RESTRICT, related_name='songs')   

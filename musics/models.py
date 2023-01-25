from django.db import models
from .validators import image_size, music_size, music_type
from django.conf import settings
from django.utils.text import slugify


class Profile(models.Model):
    # Normal users can be upgrade
    SILVER_USER = 's'
    GOLD_USER = 'g'
    DIAMOND_USER = 'd'
    USER_MODE = [
        (SILVER_USER, 'silver'),
        (GOLD_USER, 'gold'),
        (DIAMOND_USER, 'diamond')
    ]

    image = models.ImageField(
        upload_to='media/profie-images', validators=[image_size])
    user_mode = models.CharField(
        max_length=1, choices=USER_MODE, default=SILVER_USER)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # Just artists can be verified
    is_verified = models.BooleanField(
        default=False)

    # Normal users and artists can be upgrade
    is_upgraded = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True,
                            blank=False, null=False, db_index=True)

    def save(self, *args, **kwargs):

        self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """
        Generate a unique slug using the user's username
        """
        slug = slugify(self.user.username)
        unique_slug = slug
        num = 1
        while Profile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def __str__(self):
        return slugify(self.user.username)


class Album(models.Model):
    title = models.CharField(
        max_length=255, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='albums')
    slug = models.SlugField(max_length=255, unique=True,
                            blank=False, null=False, db_index=True)

    def save(self, *args, **kwargs):

        self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """
        Generate a unique slug using the user's username
        """
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Profile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def __str__(self):
        return slugify(self.title)


class Song(models.Model):
    music_file = models.FileField(
        upload_to='media/songs', validators=[music_type, music_size])
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, models.RESTRICT, related_name='songs')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# class COMMAND(models.Model):
#     song = models.ForeignKey(
#         Song, on_delete=models.CASCADE, related_name='commands')
#     text = models.CharField()
#     created_at = models.DateTimeField(auto_now_add=True

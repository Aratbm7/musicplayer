from django.core.exceptions import ValidationError


def image_size(image):
    max_size = 2
    if image.size > (max_size * 1048576):
        raise ValidationError(f'Image size must be less than {max_size} MiB!')



def music_size(music):
    max_size = 15
    if music.size > (max_size * 1048576):
        raise ValidationError(f'Music size must be less than {max_size} MiB!')


def music_type(music):
    file_type = '.mp3'
    if file_type not in music.name:
        raise ValidationError(f'uploaded file must be {file_type} file!!') 
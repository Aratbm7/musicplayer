# Generated by Django 4.1.4 on 2023-02-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0005_alter_album_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='slug',
            field=models.SlugField(default='-', max_length=500, unique=True),
            preserve_default=False,
        ),
    ]
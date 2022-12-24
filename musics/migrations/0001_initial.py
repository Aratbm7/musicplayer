# Generated by Django 4.1.4 on 2022-12-19 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import musics.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('image', models.ImageField(upload_to='media/profie-images', validators=[musics.validators.image_size])),
                ('user_mode', models.CharField(choices=[('a', 'artist'), ('c', 'customer')], default='c', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_file', models.FileField(upload_to='media/songs', validators=[musics.validators.music_type, musics.validators.music_size])),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='songs', to='musics.album')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='musics.profile')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musics.profile'),
        ),
    ]

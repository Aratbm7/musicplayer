from .models import Profile, Album
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ProfileSerilizer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'image', 'user_mode',
                  'is_verified', 'is_upgraded', 'slug']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class PutProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Profile
        fields = ('image', 'user_id', 'slug')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class AlbumSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'created_at', 'profile_id', 'slug', 'songs']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
    # def create(self, validated_data):
    #     user_id = self.context['request'].user.id
    #     profile_id = Profile.objects.get(user_id=user_id).id

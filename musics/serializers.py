from .models import Profile, Album, Song
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from django.contrib.auth import get_user_model


class UserDomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'is_active', 'url')
        extra_kwargs = {
            'url': {'lookup_field': 'id'}}


class ProfileSerilizer(serializers.ModelSerializer):
    user = UserDomainSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'image', 'user_mode',
                  'is_verified', 'is_upgraded', 'slug', 'user']
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


class ProfilelDomainSerializer(serializers.HyperlinkedModelSerializer):
    user = UserDomainSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'url', 'image', 'user',
                  'user_mode', 'is_verified', 'is_upgraded', 'slug']
        extra_kwargs = {
            'url': {'view_name': 'profiles-detail', 'lookup_field': 'slug'}, }


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.SlugField(read_only=True)
    profile = ProfilelDomainSerializer(read_only=True)
    songs = NestedHyperlinkedRelatedField(
        many=True, read_only=True,
        view_name='albums_songs-detail',
        lookup_field='slug',
        parent_lookup_kwargs={'album_slug': 'album__slug'}
    )

    class Meta:
        model = Album
        fields = ['id', 'title', 'created_at',
                  'profile', 'slug', 'songs']
        extra_kwargs = {
            'url': {'lookup_field': 'slug', }
        }
    # def create(self, validated_data):
    #     user_id = self.context['request'].user.id
    #     profile_id = Profile.objects.get(user_id=user_id).id


class AlbumSerializerForSong(NestedHyperlinkedModelSerializer):
    class Meta:
        model = Album
        fields = ['url', 'id', 'title', 'created_at',
                  'profile_id', 'slug']
        extra_kwargs = {
            'url': {'view_name': 'albums-detail', 'lookup_field': 'slug'}}


class SongSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    album = AlbumSerializerForSong(read_only=True)
    profile = ProfilelDomainSerializer(read_only=True)
    parent_lookup_kwargs = {
        'album_slug': 'album__slug'
    }

    class Meta:
        model = Song
        fields = ['id', 'music_file', 'uploaded_at',
                  'album', 'slug', 'profile']
        extra_kwargs = {
            'url': {'lookup_field': 'album_slug'},
        }

    def validate(self, attrs):
        self.validate_dict = super(SongSerializer, self).validate(attrs)
        profile_albums_list = get_object_or_404(
            Profile, user_id=self.context.get("user_id", None)).albums.all().values_list("id", flat=True)
        album_id = get_object_or_404(
            Album, slug=self.context.get('album_slug', None)).id
        if not bool(album_id in profile_albums_list):
            raise serializers.ValidationError("you can just edit own albums")
        return self.validate_dict

    def create(self, validated_data):
        user_id = self.context['user_id']
        profile_id = Profile.objects.get(user_id=user_id).id
        album_slug = self.context['album_slug']
        album_id = Album.objects.get(slug=album_slug).id
        return Song.objects.create(profile_id=profile_id, album_id=album_id, **validated_data)

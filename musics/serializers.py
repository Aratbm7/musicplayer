from .models import Profile, Album, Song
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


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


# class SongsHyperlink(serializers.HyperlinkedRelatedField):
#     # We define these as class attributes, so we don't need to pass them as arguments.
#     view_name = 'album-songs-detail'
#     queryset = Song.objects.all()

#     def get_url(self, obj, view_name, request, format):
#         url_kwargs = {
#             'id': obj.id,
#             'album_pk': obj.pk
#         }
#         return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

#     def get_object(self, view_name, view_args, view_kwargs):
#         lookup_kwargs = {
#             '': view_kwargs['organization_slug'],
#             'pk': view_kwargs['customer_pk']
#         }
#         return self.get_queryset().get(**lookup_kwargs)


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    profile_id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    # songs = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, lookup_field='pk', view_name='albums_songs_detail')
    # songs = serializers.HyperlinkedIdentityField(
    #     view_name='albums_songs-list',
    #     lookup_field='slug',
    #     lookup_url_kwarg='album_slug', read_only=True,

    # )

    songs = NestedHyperlinkedRelatedField(
        many=True, read_only=True,
        view_name='albums_songs-detail',
        lookup_field='slug',
        parent_lookup_kwargs={'album_slug': 'album__slug'}
    )

    class Meta:
        model = Album
        fields = ['id', 'title', 'created_at',
                  'profile_id', 'slug', 'songs']
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

    # album = NestedHyperlinkedRelatedField(
    #     view_name='albums-detail',
    #     lookup_field='slug',
    #     read_only=True
    # )
    album = AlbumSerializerForSong(read_only=True)
    parent_lookup_kwargs = {
        'album_slug': 'album__slug'
    }

    class Meta:
        model = Song
        fields = ['id', 'music_file', 'uploaded_at',
                  'profile_id', 'album', 'slug']
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

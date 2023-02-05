from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ProfileSerilizer, PutProfileSerializer, AlbumSerializer, SongSerializer)
from rest_framework import permissions
from .permissions import ProfilePermissions, AlbumPermissions, SongPermissions, personal_permissions
from .models import (Profile, Album, Song)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete', 'option']
    queryset = Profile.objects.select_related('user').all()
    permission_classes = [ProfilePermissions]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return PutProfileSerializer
        return ProfileSerilizer

    # def retrieve(self, request, slug):
    #     permission_classes = [permissions.IsAdminUser]
    #     profile = get_object_or_404(Profile, slug=slug)
    #     serializer = self.get_serializer(profile)
    #     return Response(serializer.data)

    @action(detail=False, methods=['get', 'put', 'delete'], permission_classes=[permissions.IsAuthenticated],
            )
    def me(self, request):
        user_id = self.request.user.id
        (profile, created) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfileSerilizer(profile)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PutProfileSerializer(
                profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            Profile.objects.get(user_id=user_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        def perform_update(self, serializer):
            return serializer.save(user_id=user_id)

        def get_serializer_context(self):
            print(self.request.method)
            context = super(ProfileViewSet, self).get_serializer_context()
            return context.update({'request': self.request})


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.select_related('profile')\
        .prefetch_related('songs').all()
    serializer_class = AlbumSerializer
    permission_classes = [personal_permissions(
        {'u': 63, 'o': 3}), AlbumPermissions]
    lookup_field = 'slug'

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [permissions.IsAuthenticated()]

    #     # if self.request.method in ['PUT', 'PATCH', 'DELETE']:
    #     #     return [permissions.DjangoObjectPermissions()]
    #     return super(AlbumViewSet, self).get_permissions()

    # def get_serializer_context(self):
    #     return {'request': self.request}

    def perform_create(self, serializer):
        user_id = self.request.user.id
        profile_id = Profile.objects.get(user_id=user_id).id
        return serializer.save(profile_id=profile_id)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_albums(self, request):

        if request.method == 'GET':
            profile_id = Profile.objects\
                .get(user_id=request.user.id).id

            my_albums = Album.objects.prefetch_related('songs')\
                .select_related('profile')\
                .filter(profile_id=profile_id)

            serializer = AlbumSerializer(my_albums, many=True)
            return Response(serializer.data)


class SongViewSet(ModelViewSet):
    http_method_names = ['post', 'get', 'options', 'heade', 'delete']
    serializer_class = SongSerializer
    permission_classes = [SongPermissions]
    lookup_field = 'slug'

    def get_queryset(self):
        return Song.objects.filter(album__slug=self.kwargs['album_slug'])

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'album_slug': self.kwargs['album_slug'], 'request': self.request}

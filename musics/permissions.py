from rest_framework import permissions
from .models import Profile, Album
from django.shortcuts import get_object_or_404
from django.db.models import Q
from math import log2
from collections import defaultdict


action_dict = {
    'retrieve': 1,
    'list': 2,
    'partially_update': 4,
    'update': 8,
    'create': 16,
    'destroy': 32,
    # for all 63
}


def return_view_action_lists(input_dict, client_type):
    if input_dict[client_type] == 0:
        return []
    x = int(log2(input_dict[client_type] + 1))
    return tuple(action_dict.keys())[:x]


def personal_permissions(input_dict):
    send_dict = defaultdict(lambda: 63)
    print(send_dict)
    print('-' * 60)
    send_dict.update(input_dict)

    class CustomPermisson(permissions.BasePermission):

        def has_permission(self, request, view):
            user_permisson_list = return_view_action_lists(send_dict, 'u')
            admin_permisson_list = return_view_action_lists(send_dict, 'a')
            other_permisson_list = return_view_action_lists(send_dict, 'o')

            if request.user and request.user.is_authenticated:
                if view.action in user_permisson_list:
                    return True
                else:
                    return False

            elif request.user.is_staff:
                if view.action in admin_permisson_list:
                    return True

            elif not request.user.is_authenticated:
                if view.action in other_permisson_list:
                    return True

    return CustomPermisson


class ProfilePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not bool(request.user.is_authenticated):
            return False

        if view.action in ['retrieve', 'update', 'partial_update']:
            profile = Profile.objects.select_related('user')\
                .get(user_id=request.user.id)
            return bool(profile == obj or request.user.is_staff)

        elif view.action == 'destroy':
            return request.user.is_staff
        else:

            return False


class AlbumPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if view.action in ['retrieve', 'update', 'partially_update', 'destroy']:
            profile_id = get_object_or_404(Profile, user_id=request.user.id).id
            # profile_id = Profile.objects.select_related('user')\
            #     .get(user_id=request.user.id).id
            album = get_object_or_404(
                Album, profile_id=profile_id, slug=view.kwargs['slug'])
            print(view.kwargs['slug'])
            return bool(obj == album or request.user.is_staff)

        return False


class SongPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True

        elif view.action in ['create', 'destroy']:
            profile_albums_list = get_object_or_404(
                Profile, user_id=request.user.id).albums.all().values_list("id", flat=True)
            album_id = get_object_or_404(
                Album, slug=view.kwargs['album_slug']).id
            return bool(request.user.is_authenticated and
                        album_id in profile_albums_list)
        else:
            return False

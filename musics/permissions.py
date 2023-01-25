from rest_framework import permissions
from .models import Profile, Album
from django.shortcuts import get_object_or_404
from django.db.models import Q


class ProfilePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        # viiew.actions are (list, create, retrieve, update, partial_update, destroy)
        # request.methods are (get, post, patch, put, delete, options)
        if view.action == 'list':
            return bool(request.user and request.user.is_staff)

        elif view.action == 'create':
            return bool(request.user and request.user.is_authenticated)

        elif view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return True
        else:
            return False

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

    def has_permission(self, request, view):
        if view.action == 'list':
            return True

        elif view.action == 'create':
            return bool(request.user.is_authenticated)

        elif view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return True

        return False

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

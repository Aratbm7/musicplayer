from django.urls import path, include
from rest_framework.routers import Route, DynamicRoute, DefaultRouter
from .views import (ProfileViewSet, AlbumViewSet)


# class CustomRouter(DefaultRouter):
#     routes = [
#         Route(
#             url=r'^{prefix}/{lookup}/$',
#             mapping={'get': 'retrieve_by_username'},
#             name='{basename}-username',
#             detail=False,
#             initkwargs={'suffix': 'Username'}
#         ),
#         DynamicRoute(
#             url=r'^{prefix}/{lookup}/{url_path}$',
#             name='{basename}-{url_name}',
#             detail=False,
#             initkwargs={}
#         )
#     ]


router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('albums', AlbumViewSet, basename='alubms')

urlpatterns = [
    path('', include(router.urls)),

]

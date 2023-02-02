from django.urls import path, include
# from rest_framework.routers import Route, DynamicRoute, DefaultRouter
from rest_framework_nested import routers
from .views import (ProfileViewSet, AlbumViewSet, SongViewSet)


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


router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('albums', AlbumViewSet, basename='albums')

album_router = routers.NestedDefaultRouter(router, 'albums', lookup='album')
album_router.register('songs', SongViewSet, basename='albums_songs')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(album_router.urls), name='song-detail'),

]

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Album
from .serializers import AlbumSerializer
import os


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_fields = ['artist', 'file_format', 'is_on_device']
    ordering_fields = ['artist', 'album', 'file_format']
    ordering = ['artist']
    search_fields = ['artist', 'album', 'file_format']

    @action(methods=['GET'], detail=False)
    def get_artist_list(self, request):
        return Response(Album.objects.all().values_list('artist', flat=True).distinct(), status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False)
    def sync_with_music_library(self, request):
        if not os.path.exists(settings.MUSIC_COLLECTION_ROOT_DIR):
            return Response('Plug in your hard drive!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['GET'], detail=False)
    def sync_with_device(self, request):
        if not os.path.exists(settings.DEVICE_ROOT_DIR):
            return Response('Plug in your mp3 player!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

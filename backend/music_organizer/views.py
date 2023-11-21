from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.core.cache import cache
from .models import Album
from .serializers import AlbumSerializer
from .func import sync_with_music_library, sync_device
from uuid import uuid4
import os
import threading


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
        total = 0
        for artist in os.listdir(settings.MUSIC_COLLECTION_ROOT_DIR):
            total += len(os.listdir(os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, artist)))
        job_id = uuid4()
        cache.set(job_id, {'total': total, 'completed': 0})
        t = threading.Thread(target=sync_with_music_library,
                            args=[job_id])
        t.setDaemon(True)
        t.start()
        return Response(job_id, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def sync_with_device(self, request):
        if not os.path.exists(settings.DEVICE_ROOT_DIR):
            return Response('Plug in your mp3 player!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not os.path.exists(settings.MUSIC_COLLECTION_ROOT_DIR):
            return Response('Plug in your hard drive!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        job_id = uuid4()
        cache.set(job_id, {'total': len(request.data['ids']), 'completed': 0})
        t = threading.Thread(target=sync_device,
                            args=[job_id, request.data['ids']])
        t.setDaemon(True)
        t.start()
        return Response(job_id, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False)
    def get_sync_progress(self, request):
        key = str(request.data['key'])
        progress = cache.get(key)
        if progress is None:
            return Response('Failed to get progress', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(progress, status=status.HTTP_200_OK)

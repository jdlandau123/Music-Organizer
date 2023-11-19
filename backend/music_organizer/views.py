from rest_framework import viewsets
from .models import Album
from .serializers import AlbumSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filterset_fields = ['artist', 'file_format', 'is_on_device']
    ordering_fields = ['artist', 'album', 'file_format']
    ordering = ['artist']
    search_fields = ['artist', 'album', 'file_format']

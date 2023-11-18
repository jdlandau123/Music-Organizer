from rest_framework import viewsets
from .models import Album
from .serializers import AlbumSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('artist')
    serializer_class = AlbumSerializer

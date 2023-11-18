from django.core.management.base import BaseCommand
from django.conf import settings
from music_organizer.models import Album
from pathlib import Path
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Populating Database...')
        
        for artist in os.listdir(settings.MUSIC_COLLECTION_ROOT_DIR):
            print(artist)
            for album in os.listdir(os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, artist)):
                album_path = os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, artist, album)
                f = Path(os.listdir(album_path)[0]).suffix.replace('.', '').upper()
                tracks = {}
                for index, song in enumerate(os.listdir(album_path)):
                    song_path = Path(os.path.join(album_path, song))
                    tracks[index + 1] = song_path.with_suffix('').name
                Album.objects.create(artist=artist, album=album, format=f, tracklist=tracks)

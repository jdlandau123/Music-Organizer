from django.core.cache import cache
from django.conf import settings
from pathlib import Path
from .models import Album
import os
import shutil

def sync_with_music_library(job_id):
    for artist in os.listdir(settings.MUSIC_COLLECTION_ROOT_DIR):
        for album in os.listdir(os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, artist)):
            album_path = os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, artist, album)
            f = Path(os.listdir(album_path)[0]).suffix.replace('.', '').upper()
            tracks = {}
            for index, song in enumerate(os.listdir(album_path)):
                song_path = Path(os.path.join(album_path, song))
                if song_path.suffix in ['.mp3', '.flac', 'wav']:
                    tracks[index + 1] = song_path.with_suffix('').name
            Album.objects.update_or_create(artist=artist, album=album,
                                           defaults={'artist':artist, 'album':album, 'file_format':f, 'tracklist':tracks})
            progress = cache.get(job_id)
            progress['completed'] += 1
            cache.set(job_id, progress)
    
    for a in Album.objects.all():
        if not os.path.exists(os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, a.artist, a.album)):
            a.delete()
    
    progress = cache.get(job_id)
    progress['completed'] = progress['total']
    cache.set(job_id, progress)


def sync_device(job_id, album_ids_to_sync):
    for artist in os.listdir(settings.DEVICE_ROOT_DIR):
        if os.path.isdir(os.path.join(settings.DEVICE_ROOT_DIR, artist)):
            for album in os.listdir(os.path.join(settings.DEVICE_ROOT_DIR, artist)):
                album_record = Album.objects.filter(artist=artist, album=album).first()
                if album_record is None:
                    continue
                if album_record.id not in album_ids_to_sync:
                    album_record.is_on_device = False
                    album_record.save()
                    shutil.rmtree(os.path.join(settings.DEVICE_ROOT_DIR, artist, album))

    for album_id in album_ids_to_sync:
        album = Album.objects.get(pk=album_id)
        if not os.path.exists(os.path.join(settings.DEVICE_ROOT_DIR, album.artist, album.album)):
            album_path = os.path.join(settings.MUSIC_COLLECTION_ROOT_DIR, album.artist, album.album)
            shutil.copytree(album_path, os.path.join(settings.DEVICE_ROOT_DIR, album.artist, album.album), dirs_exist_ok=True)
            album.is_on_device = True
            album.save()
        progress = cache.get(job_id)
        progress['completed'] += 1
        cache.set(job_id, progress)
    
    for artist in os.listdir(settings.DEVICE_ROOT_DIR):
        artist_folder = os.path.join(settings.DEVICE_ROOT_DIR, artist)
        if os.path.isdir(artist_folder) and len(os.listdir(artist_folder)) == 0:
            os.rmdir(artist_folder)
    
    progress = cache.get(job_id)
    progress['completed'] = progress['total']
    cache.set(job_id, progress)

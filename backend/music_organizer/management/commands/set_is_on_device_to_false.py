from django.core.management.base import BaseCommand
from music_organizer.models import Album

class Command(BaseCommand):
    def handle(self, *args, **options):
        Album.objects.all().update(is_on_device=False)

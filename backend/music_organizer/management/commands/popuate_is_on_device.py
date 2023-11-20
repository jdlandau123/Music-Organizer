from django.core.management.base import BaseCommand
from django.conf import settings
from music_organizer.models import Album
from pathlib import Path
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Command for populating album is_on_device field
        """
        print('Updating Albums...')

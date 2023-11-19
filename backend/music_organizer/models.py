from django.db import models

FORMAT_CHOICES = (
    ('MP3', 'MP3'),
    ('FLAC', 'FLAC')
)

# Consider adding mutagen for a bitrate / other tag fields
# https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python
class Album(models.Model):
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    file_format = models.CharField(choices=FORMAT_CHOICES, default='MP3', max_length=4)
    tracklist = models.JSONField()
    is_on_device = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.artist} - {self.album}"

from celery import shared_task
from django.core.cache import cache

@shared_task()
def sync_music_library_task(job_id):
    """
    the goal here is to just loop through music library and update the db. use update or create for album records.
    total will be the number of albums in collection.
    """
    value = cache.get(job_id)
    print('SYNCING')
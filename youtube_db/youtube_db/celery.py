from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

import youtube_dl

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_db.settings')

app = Celery('youtube_db')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, download)


@app.task
def download():
    from .models import DLQueue
    to_download = DLQueue.objects.filter(status=1).first()
    if not to_download:
        return
    to_download.status = 2
    to_download.save(update_fields=['status'])

    def dl_hook(d):
        print(d)
        if d['status'] == 'finished':
            to_download.status = 3
            to_download.title = d['filename']
            to_download.save(update_fields=['status', 'title'])
            os.rename(to_download.title,
                      'storage/{}'.format(to_download.title))
    ydl_opts = {
        'progress_hooks': [dl_hook]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([to_download.youtube_url])

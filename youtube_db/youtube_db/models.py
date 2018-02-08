from django.db import models
from django.conf import settings


DL_STATUS_CHOICES = (
    (1, 'Pending'),
    (2, 'Inprogress'),
    (3, 'Downloaded Server'),
    (4, 'Downloaded Mobile'),
    (5, 'Failed')
)


class DLQueue(models.Model):
    youtube_url = models.URLField()
    status = models.PositiveIntegerField(choices=DL_STATUS_CHOICES, default=1)
    title = models.CharField(max_length=255, blank=True)
    when = models.DateTimeField(auto_now_add=True)
    when_updated = models.DateTimeField(auto_now=True)

    def url(self, domain):
        return 'http://{}{}{}'.format(domain, settings.MEDIA_URL, self.title)

from django.contrib import admin

from .models import DLQueue


class DLQueueAdmin(admin.ModelAdmin):
    model = DLQueue
    list_display = (
        'youtube_url', 'status', 'title', 'when')


admin.site.register(DLQueue, DLQueueAdmin)

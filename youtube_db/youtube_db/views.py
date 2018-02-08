from django.views.generic import View, TemplateView
from django.http import JsonResponse

from .models import DLQueue


class QueueVideoView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        url = self.request.GET.get('url')
        if url and not DLQueue.objects.filter(
                youtube_url=url, status__lte=3).exists():
            DLQueue.objects.create(youtube_url=url)
        return {'objects': DLQueue.objects.filter(
            status__lte=3).order_by('-when')}


class ListServerDownloaded(View):

    def get(self, request):
        print(request.META)
        data = [{'id': obj.pk,
                 'url': obj.url(request.META['HTTP_HOST']),
                 'title': obj.title.split('.')[0]}
                for obj in DLQueue.objects.filter(status=3).iterator()]
        return JsonResponse(data, safe=False)


class MarkDownloaded(View):

    def get(self, request):
        id = request.GET.get('id', 0)
        dl = DLQueue.objects.filter(id=id, status=3).first()
        if dl:
            dl.status = 4
            dl.save(update_fields=['status'])
        return JsonResponse({})

from django.http import HttpResponse

from temperatures.models import Probe


def index(request):
    probes = Probe.objects.order_by('-timestamp')
    return HttpResponse(probes)

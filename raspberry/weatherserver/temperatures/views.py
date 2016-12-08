from django.http import HttpResponse

from temperatures.models import Probe


def index(request):
    probes = "\n".join(str(x) for x in Probe.objects.order_by('-timestamp'))
    return HttpResponse(probes)

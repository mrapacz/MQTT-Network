from django.http import HttpResponse
from django.shortcuts import render

from temperatures.models import Probe


def index(request):
    probes = Probe.objects.order_by('-timestamp')
    return render(request, 'temperatures/index.html', {'probes': probes})

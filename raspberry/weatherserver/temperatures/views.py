from datetime import datetime, timedelta
from chartit import Chart
from chartit import DataPool
from django.shortcuts import render
from django.utils import timezone

from temperatures.models import Probe
from weatherserver import settings
import pytz


def tz_oriented_date(date):
    DATE_FORMAT = "%H:%M, %d %b"
    converted_date = date.astimezone(pytz.timezone(settings.TIME_ZONE))
    return datetime.strftime(converted_date, DATE_FORMAT)


def get_recent_probes(node_id):
    print("ID IZ")
    print(node_id)
    probes = Probe.objects.all().filter(timestamp__gte=timezone.now() - timedelta(days=1,), node_id=node_id)
    for probe in probes:
        print(probe)
    return probes


def index(request):
    nodes = list(Probe.objects.values_list('node_id').distinct())

    ds = DataPool(
        series=[{
                    'options': {'source': get_recent_probes(node_id)},
                    'terms':
                        [
                            {'timestamp - ' + str(node_id): 'timestamp'},
                            {'temperature - ' + str(node_id): 'temperature'},
                        ]
                } for (node_id,) in nodes])

    cht = Chart(
        datasource=ds,
        series_options=
        [{
            'options':
                {
                    'type': 'line',
                    'stacking': False,
                },
            'terms': {'timestamp - ' + str(node_id): ['temperature - ' + str(node_id)] for (node_id,) in nodes}
        }],
        chart_options=
        {
            'title': {'text': 'Temperature chart'},
            'xAxis': {'title': {'text': 'Time'}},
            # -*- coding: utf-8 -*-
            'yAxis': {'title': {'text': 'Temperature (°C)'}}

        },
        x_sortf_mapf_mts=(None, tz_oriented_date, False)
    )

    # -*- coding: utf-8 -*-
    last_probe = Probe.objects.order_by('-timestamp')[0]
    last_measured = "{}°C".format(last_probe.temperature)
    last_date = tz_oriented_date(last_probe.timestamp)
    return render(request, 'temperatures/index.html',
                  {'last_measured': last_measured, 'last_date': last_date, 'chart': cht})

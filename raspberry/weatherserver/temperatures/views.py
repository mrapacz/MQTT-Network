from datetime import datetime, timedelta
from itertools import groupby
from statistics import mean

from chartit import Chart
from chartit import DataPool
from django.shortcuts import render
from django.utils import timezone
from random import choice

from temperatures.models import Probe
from weatherserver import settings
import pytz


def tz_oriented_date(date):
    DATE_FORMAT = "%H:%M, %d %b"
    converted_date = date.astimezone(pytz.timezone(settings.TIME_ZONE))
    return datetime.strftime(converted_date, DATE_FORMAT)


def get_recent_probes(node_id):
    # print("ID IZ")
    # print(node_id)
    probes = Probe.objects.all().filter(timestamp__gte=timezone.now() - timedelta(days=1, ), node_id=node_id).order_by(
        'timestamp')
    # for probe in probes:
    #     print(probe)
    return probes


def get_avg_probes(node_id):
    probes = get_recent_probes(node_id)
    grouped_probes = groupby(probes, key=lambda probe: (
        probe.timestamp.hour, probe.timestamp.minute - probe.timestamp.minute % 20))

    grouped_probes = [(key, list(group)) for key, group in grouped_probes]

    timestamps = [probe_group[0].timestamp for _, probe_group in grouped_probes]
    timestamps = [timestamp.replace(minute=timestamp.minute - timestamp.minute % 20) for timestamp in timestamps]
    avg_temperatures = [mean(probe.temperature for probe in probe_group) for _, probe_group in grouped_probes]
    print(timestamps)
    print(avg_temperatures)
    chart_probes = [Probe(timestamp=timestamp, temperature=avg_temperature, node_id=node_id) for
                    (timestamp, avg_temperature) in
                    zip(timestamps, avg_temperatures)]
    print(chart_probes)

    print('*' * 60)
    return chart_probes


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
                    # 'dashStyle': 'longdash'
                    'zones': [{
                        'value': 19.5,
                        'color': '#f7a35c'
                    }, {
                        'value': 19.6,
                        'color': '#7cb5ec'
                    }, {
                        'color': '#90ed7d'
                    }]
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

from datetime import datetime, timedelta
from chartit import Chart
from chartit import DataPool
from django.shortcuts import render
from django.utils import timezone

from temperatures.models import Probe
from weatherserver import settings
import pytz


def tzoriented_date(date):
    DATE_FORMAT = "%H:%M, %d %b"
    converted_date = date.astimezone(pytz.timezone(settings.TIME_ZONE))
    return datetime.strftime(converted_date, DATE_FORMAT)


def index(request):
    print(timezone.now())
    ds = DataPool(
        series=
        [{
            'options': {'source': Probe.objects.all().filter(timestamp__gte=timezone.now() - timedelta(days=1))},
            'terms':
                [
                    'timestamp',
                    'temperature',
                ]
        }])

    cht = Chart(
        datasource=ds,
        series_options=
        [{
            'options':
                {
                    'type': 'line',
                    'stacking': False,
                },
            'terms': {'timestamp': ['temperature', ]}
        }],
        chart_options=
        {
            'title': {'text': 'Temperature chart'},
            'xAxis': {'title': {'text': 'Time'}}
        },
        x_sortf_mapf_mts=(None, tzoriented_date, False)
    )
    probes = Probe.objects.order_by('-timestamp')
    return render(request, 'temperatures/index.html', {'probes': probes, 'chart': cht})

from statistics import mean

from django.utils import timezone
from weatherserver.utils.dumper_setup import Probe, DoesNotExist, MultipleObjectsReturned
from datetime import datetime


def dump_data(node_id, temperature):
    time = timezone.now()
    time = time.replace(minute=(time.minute - time.minute % 10), second=0, microsecond=0)

    try:
        p = Probe.objects.get(timestamp=time)
        p.temperature = mean(temperature, p.temperature)
        p.save()
    except DoesNotExist:
        p = Probe(node_id=node_id, temperature=temperature, timestamp=time)
        p.save()
    except MultipleObjectsReturned:
        print("More than two probes during the last 10 minutes!")

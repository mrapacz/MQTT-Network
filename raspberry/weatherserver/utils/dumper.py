from django.utils import timezone
from weatherserver.utils.dumper_setup import Probe
from datetime import datetime


def dump_data(node_id, temperature):
    time = timezone.now()
    time = time.replace(second=0, microsecond=0)
    p = Probe(node_id=node_id, temperature=temperature, timestamp=time)
    p.save()
    print(p)

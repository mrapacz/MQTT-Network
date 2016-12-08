from django.db import models
from datetime import datetime
from django.utils import timezone


class Probe(models.Model):
    node_id = models.IntegerField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " ".join((str(x) for x in [self.node_id, self.temperature, self.timestamp]))

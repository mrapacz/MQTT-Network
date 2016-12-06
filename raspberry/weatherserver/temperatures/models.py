from django.db import models
from datetime import datetime


class Probe(models.Model):
    node_id = models.SmallIntegerField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(default=datetime.now)

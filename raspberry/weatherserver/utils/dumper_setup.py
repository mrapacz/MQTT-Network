import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'weatherserver.weatherserver.settings'
django.setup()
from temperatures.models import Probe, DoesNotExist, MultipleObjectsReturned

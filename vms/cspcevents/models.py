from django.db import models
from schedule.models import Event, EventRelation, Calendar
from vms.locations.models import Location

# Create your models here.
class CSPCEvent(Event):
    event_location = models.ForeignKey(Location, default=1)


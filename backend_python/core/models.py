# Third-Party Import
import uuid

# Local Imports
from django.db import models


# Create your models here.
class Event(models.Model):

    STATUS_CHOICES = (
        ('OnTime', 'OnTime'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=255, blank=False, unique=True)
    event_date = models.DateField(null=False, blank=False)
    event_location = models.CharField(max_length=255, blank=False)
    initial_tickets = models.PositiveIntegerField(null=False, blank=True)
    event_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='OnTime')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name


def generate_ticket_token():
    return str(uuid.uuid4().hex[:8])


class Ticket(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=False)
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket")
    full_name = models.CharField(max_length=255, null=True, blank=True)
    no_of_tickets = models.PositiveIntegerField(null=True, blank=True)
    redeemed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.redeemed)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_ticket_token()
        super(Ticket, self).save(*args, **kwargs)

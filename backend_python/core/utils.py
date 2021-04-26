from .models import Event, Ticket


def auto_generate_tickets(event_name, no_of_tickets=10):
    event = Event.objects.get(event_name=event_name)
    for x in range(0, no_of_tickets):
        ticket = Ticket(event_name=event)
        ticket.save()

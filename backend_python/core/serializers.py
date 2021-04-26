from rest_framework import serializers
from .models import Event, Ticket


class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    event_ticket_count = serializers.SerializerMethodField()
    redeemed_ticket_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'event_name', 'event_date', 'event_location',
                  'initial_tickets', 'event_status',
                  'event_ticket_count', 'redeemed_ticket_count')

    def get_event_ticket_count(self, obj):
        return Ticket.objects.filter(event_name=obj).count()

    def get_redeemed_ticket_count(self, obj):
        return Ticket.objects.filter(event_name=obj, redeemed=True).count()


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    event_name = serializers.CharField(source='event_name.event_name')

    class Meta:
        model = Ticket
        fields = '__all__'


class GenerateTicketSerializer(serializers.Serializer):
    event_id = serializers.CharField(max_length=255, required=True)
    no_of_tickets = serializers.IntegerField(required=True)

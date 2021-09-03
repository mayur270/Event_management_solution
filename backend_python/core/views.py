from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import (
    Event,
    Ticket
)
from .serializers import (
    EventSerializer,
    GenerateTicketSerializer,
    TicketSerializer,
)
from .utils import auto_generate_tickets


class EventGetViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventPostViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_event = Event()

        if serializer.validated_data.get('event_name'):
            new_event.event_name = serializer.validated_data[
                "event_name"]

        if serializer.validated_data.get('event_date'):
            new_event.event_date = serializer.validated_data[
                "event_date"]

        if serializer.validated_data.get('event_location'):
            new_event.event_location = serializer.validated_data[
                "event_location"]

        if serializer.validated_data.get('initial_tickets'):
            new_event.initial_tickets = serializer.validated_data[
                "initial_tickets"]

        if serializer.validated_data.get('event_status'):
            new_event.event_status = serializer.validated_data[
                "event_status"]

        new_event.save()
        auto_generate_tickets(new_event.event_name, new_event.initial_tickets)

        return Response({'success': new_event.id},
                        status=status.HTTP_201_CREATED)


class EventPutViewSet(viewsets.ViewSet):

    def put(self, request, *args, **kwargs):
        instance = Event.objects.get(id=kwargs.get('event_id'))
        serializer = EventSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EventDeleteViewSet(viewsets.ViewSet):

    def delete(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        filtered_event = Event.objects.filter(id=event_id)
        filtered_event.delete()
        return Response({"success": "Deleted"}, status=status.HTTP_200_OK)


class TicketGetViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):

        events = Ticket.objects.all()
        serializer = TicketSerializer(events, many=True)
        return Response(serializer.data)


class TicketPostViewSet(viewsets.ViewSet):

    def post(self, request):
        serializer = GenerateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auto_generate_tickets(serializer.data['event_name'],
                              serializer.data['no_of_tickets'])
        return Response({'success': serializer.data['event_name']},
                        status=status.HTTP_201_CREATED)


class TicketDeleteViewSet(viewsets.ViewSet):

    def delete(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        filtered_ticket = Ticket.objects.filter(id=ticket_id)
        filtered_ticket.delete()
        return Response({"success": "Deleted"}, status=status.HTTP_200_OK)


class RedeemViewSet(viewsets.ViewSet):

    def get(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')

        if Ticket.objects.filter(id=ticket_id, redeemed=True):
            return Response({"gone": "Ticket has already been redeemed"},
                            status=status.HTTP_410_GONE)

        Ticket.objects.filter(id=ticket_id).update(redeemed=True)
        return Response({"success": ""}, status=status.HTTP_200_OK)

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Event


class TestEvent(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.event_1 = Event.objects.create(event_name='Summer Festival',
                                            event_date='2021-04-22',
                                            initial_tickets='5',
                                            event_location='Birmingham',
                                            event_status='OnTime')

        self.event_2 = Event.objects.create(event_name='Christmas',
                                            event_date='2021-12-25',
                                            initial_tickets='2',
                                            event_location='London',
                                            event_status='Cancelled')

    def teardown(self):
        Event.objects.all().delete()

    def test_event_get_view(self):
        """
        Class: EventGetViewSet
        Desc: Getting list of all events
        """

        url = reverse('events')
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(resp_obj), 2)

    def test_event_post_view(self):
        """
        Class: EventPostViewSet
        Desc: Creating a new event
        """

        data = {'event_name': 'Boxing Day',
                'event_date': '2021-12-26',
                'initial_tickets': '2',
                'event_location': 'London',
                'event_status': 'OnTime'}

        url = reverse('create-event')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 201)
        self.assertEquals(len(resp_obj), 1)

    def test_event_post_view_unique_name(self):
        """
        Class: EventPostViewSet
        Desc: 400 Error - Adding new event_name with same name is not permitted
        """

        data = {'event_name': 'Christmas',
                'event_date': '2021-12-25',
                'initial_tickets': '2',
                'event_location': 'London',
                'event_status': 'Cancelled'}

        url = reverse('create-event')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(resp_obj, {'event_name':  ['event with this event '
                                                     'name already exists.']})

    def test_event_put_view(self):
        """
        Class: EventPutViewSet
        Desc: Editing/ Updating an event
        """

        data = {'event_name': self.event_1.event_name,
                'event_date': '2021-12-30',
                'initial_tickets': self.event_1.initial_tickets,
                'event_location': self.event_1.event_location,
                'event_status': 'OnTime'}

        url = reverse('edit-event', args=[self.event_1.id])
        response = self.client.put(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj['event_status'], 'OnTime')
        self.assertEquals(resp_obj['event_date'], '2021-12-30')

    def test_event_delete_view(self):
        """
        Class: EventDeleteViewSet
        Desc: Deleting an event
        """

        # Checking if its deleted
        url = reverse('delete-event', args=[self.event_1.id])
        response = self.client.delete(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj, {'success': 'Deleted'})

        # Checking if the deleted task exists
        url = reverse('events')
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(resp_obj), 1)  # Only one event should exist
        self.assertNotEqual(resp_obj[0]['id'], 1)  # ID should not match 1

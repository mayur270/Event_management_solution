from django.urls import path

from .views import (
    EventDeleteViewSet,
    EventGetViewSet,
    EventPostViewSet,
    EventPutViewSet,
    RedeemViewSet,
    TicketDeleteViewSet,
    TicketGetViewSet,
    TicketPostViewSet
)

urlpatterns = [
    # Events
    path('events/', EventGetViewSet.as_view(
        {'get': 'list'}), name='events'),
    path('create-event/', EventPostViewSet.as_view(
        {'post': 'create'}), name='create-event'),
    path('edit-event/<str:event_id>/', EventPutViewSet.as_view(
        {'put': 'put'}), name='edit-event'),
    path('delete-event/<str:event_id>/', EventDeleteViewSet.as_view(
        {'delete': 'delete'}), name='delete-event'),

    # Tickets
    path('tickets/', TicketGetViewSet.as_view(
        {'get': 'list'}), name='tickets'),
    path('create-ticket/', TicketPostViewSet.as_view(
        {'post': 'post'}), name='create-ticket'),
    path('delete-ticket/<str:ticket_id>/', TicketDeleteViewSet.as_view(
        {'delete': 'delete'}), name='delete-ticket'),

    # Redeem Ticket
    path('redeem/<str:ticket_id>/', RedeemViewSet.as_view(
        {'get': 'get'}), name='redeem-ticket'),
]

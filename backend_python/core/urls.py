from django.urls import path
from .views import (EventGetViewSet, EventPostViewSet,
                    EventPutViewSet, EventDeleteViewSet)

urlpatterns = [
    # Events
    path('events/', EventGetViewSet.as_view({'get': 'list'}), name='events'),
    path('create-event/', EventPostViewSet.as_view({'post': 'create'}), name='create-event'),
    path('edit-event/<str:event_id>/', EventPutViewSet.as_view({'put': 'put'}), name='edit-event'),
    path('delete-event/<str:event_id>/', EventDeleteViewSet.as_view({'delete': 'delete'}), name='delete-event'),
]
from django.urls import path
from .views import DoorbellEventView, UnlockDoorView

urlpatterns = [
    path('doorbell/', DoorbellEventView.as_view(), name='doorbell-event'),
    path('unlock/<int:event_id>/', UnlockDoorView.as_view(), name='unlock-door'),
]

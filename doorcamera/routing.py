from django.urls import re_path
from .consumers import DoorbellConsumer

websocket_urlpatterns = [
    re_path(r'ws/doorbell/$', DoorbellConsumer.as_asgi()),
]

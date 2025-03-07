from django.urls import re_path
from .consumers import CameraConsumer

websocket_urlpatterns = [
    re_path(r'ws/cameras/', CameraConsumer.as_asgi()),
]

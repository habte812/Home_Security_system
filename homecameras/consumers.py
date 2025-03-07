import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Camera

class CameraConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    async def receive(self, text_data):
        cameras = Camera.objects.all().values("name", "url")
        await self.send(text_data=json.dumps({"cameras": list(cameras)}))

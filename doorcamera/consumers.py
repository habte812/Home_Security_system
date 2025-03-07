import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DoorbellConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("doorbell", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("doorbell", self.channel_name)

    async def send_doorbell_event(self, event):
        await self.send(text_data=json.dumps(event["message"]))

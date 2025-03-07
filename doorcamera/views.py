from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Doorbell
from .serializers import DoorbellSerializer
import firebase_admin
from firebase_admin import credentials, messaging

# cred = credentials.Certificate("") 
# firebase_admin.initialize_app(cred)

class DoorbellEventView(APIView):
    parser_classes = (MultiPartParser, FormParser)  #used to reseve image from the hardware part

    def post(self, request, *args, **kwargs):
        serializer = DoorbellSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.send_notification(serializer.data['image'])
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def send_notification(self, image_url):
        """Send FCM notification to the Flutter app."""
        message = messaging.Message(
            notification=messaging.Notification(
                title="Doorbell Alert!",
                body="Someone is at your door.",
                image=image_url
            ),
            topic="doorbell",
        )
        messaging.send(message)


class UnlockDoorView(APIView):
    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Doorbell, id=event_id)
        event.status = "opened"
        event.save()
        return Response({"message": "Door Unlocked"}, status=200)

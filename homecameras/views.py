from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
import cv2
from django.http import FileResponse
from .models import Camera,DetectionRequest,UserProfileImage
from .serializers import CameraSerializer, UserProfileSerializer,UserSerializer,DetectionSerializer
from rest_framework.authentication import TokenAuthentication
import numpy as np
from ultralytics import YOLO
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser


class LoginView(APIView):
    def post(self, request):
        
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    
    
class UsersCamera(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cameras = Camera.objects.filter(user=user)  # Fetch only the authenticated user's cameras

        camera_data = [
            {"id": cam.id, "name": cam.name, "url": cam.url}  # Include camera name and URL
            for cam in cameras
        ]

        return Response(camera_data, status=status.HTTP_200_OK)


class AddCameraView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        url = request.data.get('url')

        if not name or not url:
            return Response({"error": "Name and URL are required"}, status=status.HTTP_400_BAD_REQUEST)

        user_cameras = Camera.objects.filter(user=request.user)
        duplicate_count = user_cameras.filter(name__startswith=name).count()

        if duplicate_count > 0:
            name = f"{name}{duplicate_count + 1}"

        camera = Camera.objects.create(user=request.user, name=name, url=url)
        serializer = CameraSerializer(camera)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def profileImage(request):
    return FileResponse(open('C:\\Users\\User\\OneDrive\\Desktop\\laugh.jpg', 'rb'), content_type='image/jpeg')



class ObjectDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        object_to_detect = request.data.get('object_to_detect')

        if not start_time or not end_time or not object_to_detect:
            return Response({"error": "Start time, end time, and object to detect are required"}, status=status.HTTP_400_BAD_REQUEST)
      
        user_name = request.user.username  #
        custom_name = f"{user_name}-Detection Schedules" 
       
        user_schedules = DetectionRequest.objects.filter(user=request.user)
        duplicate_count = user_schedules.filter(name__startswith=custom_name).count()
        
        if duplicate_count > 0:
            custom_name = f"{custom_name}({duplicate_count + 1})"

        detection = DetectionRequest.objects.create(
            user=request.user,
            start_time=start_time,
            end_time=end_time,
            object_to_detect=object_to_detect,
            name=custom_name
        )
        
        serializer = DetectionSerializer(detection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)








original_model = YOLO("yolov8n.pt")  
trained_model = YOLO("C:\\runs\\detect\\train2\\weights\\best.pt")  

def detect_objects(frame, model):
    results = model(frame)
    detections = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            confidence = float(box.conf[0])  # Confidence score
            class_id = int(box.cls[0])  # Object class ID
            label = model.names[class_id]  # Class name

            detections.append({
                "label": label,
                "confidence": confidence,
                "bobox": (x1, y1, x2, y2)
            })

    return detections

def generate_frames():
    cap = cv2.VideoCapture(0)  

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        detections = detect_objects(frame, original_model)

        if not detections:
            detections = detect_objects(frame, trained_model)

        for det in detections:
            x1, y1, x2, y2 = det["bobox"]
            label = det["label"]
            confidence = det["confidence"]

            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

def stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')



class UpdateUserProfileView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "user": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):
    user_profile, created = UserProfileImage.objects.get_or_create(user=request.user)

    if 'image' in request.FILES:
        user_profile.image = request.FILES['image']
        user_profile.save()
        return Response({'message': 'Image uploaded successfully', 'image_url': user_profile.image.url})

    return Response({'error': 'No image provided'}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_image(request):
    user_profile = UserProfileImage.objects.get(user=request.user)
    full_image_url = request.build_absolute_uri(user_profile.image.url)
    return Response({'image_url': full_image_url})

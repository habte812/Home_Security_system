from django.urls import path
from .views import RegisterView, LoginView, ProfileView,profileImage,UsersCamera, AddCameraView,stream,ObjectDetectionView,UpdateUserProfileView,upload_profile_image,get_profile_image

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),
    
    path('stream/', stream, name='stream_camera'),
    path('add-camera/', AddCameraView.as_view(), name='add-camera'),
    path('get-camera/', UsersCamera.as_view(), name='get-camera'),
    # path('video_stream/', video_stream, name='video_feed'),
    path('object-detection/', ObjectDetectionView.as_view(), name='Object-DetectionView'),
    path('test_image/', profileImage),
    path('upload-profile-image/', upload_profile_image, name='upload_profile_image'),
    path('get-profile-image/', get_profile_image, name='get_profile_image'),

]

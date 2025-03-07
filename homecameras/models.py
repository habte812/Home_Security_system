from django.db import models
from django.contrib.auth.models import User



class Camera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cameralists')  
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class DetectionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    object_to_detect = models.CharField(max_length=255)
    name = models.CharField(max_length=255,default="User Schedules")  # Ensure this line exists

    def __str__(self):
        return self.name
    
class UserProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username
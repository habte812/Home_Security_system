from django.contrib import admin
from .models import Camera,DetectionRequest,UserProfileImage
# Register your models here.
admin.site.register(Camera)  
admin.site.register(DetectionRequest)  
admin.site.register(UserProfileImage)  

# admin.site.register(Screenshot) 
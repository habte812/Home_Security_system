from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Camera, DetectionRequest, UserProfileImage


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
     
class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'name', 'url', 'user']
        extra_kwargs = {
            'user': {'read_only': True},
        }

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionRequest
        fields = ['id', 'start_time', 'end_time', 'object_to_detect','name']
        read_only_fields = ['id', 'user', 'schedule_time']
        
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password) 

        instance.save()
        return instance
    
class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileImage
        fields = ['user', 'image']
        extra_kwargs = {'user': {'read_only': True}}
        
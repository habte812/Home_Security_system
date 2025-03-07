from rest_framework import serializers
from .models import Doorbell

class DoorbellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doorbell
        fields = '__all__'

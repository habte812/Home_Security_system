from django.db import models
from django.utils.timezone import now

class Doorbell(models.Model):
    timestamp = models.DateTimeField(default=now)
    image = models.ImageField(upload_to='guest_images/')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('opened', 'Opened')], default='pending')

    def __str__(self):
        return f"Guest at {self.timestamp}"

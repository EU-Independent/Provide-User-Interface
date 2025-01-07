from django.db import models
from django.contrib.auth.models import User
import uuid

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User model
    file_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    uploaded_file = models.FileField(upload_to='')
    timestamp = models.DateTimeField(auto_now_add=True)
    provided = models.BooleanField(default=False)  # Track if the file is provided

    def __str__(self):
        return f"{self.user.username} uploaded {self.uploaded_file} at {self.timestamp}"

class License(models.Model):
    name = models.CharField(max_length=255, unique=True)
    access_url = models.URLField()

    def __str__(self):
        return self.name
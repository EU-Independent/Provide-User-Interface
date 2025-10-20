from django.db import models
import uuid

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = self.file.name.split("/")[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or "Uploaded File"


# Model to store extracted JSON data from uploaded files
class UploadedData(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='extracted_data')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ExtractedData {self.id} for {self.file.file_name}"

class License(models.Model):
    name = models.CharField(max_length=255, unique=True)
    access_url = models.URLField()

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.oauth2 import service_account
from google.cloud import storage
from django.conf import settings
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for the user profile
    # For example:
    # bio = models.TextField(max_length=500)
    # profile_picture = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def upload_to(instance, filename):
    # Get the username from the associated user profile
    username = instance.user_profile.user.username
    
    # Remove the file extension from the original filename
    base_filename, file_extension = os.path.splitext(filename)
    
    # Construct the new unique filename using the username
    unique_filename = f"uploads/{username}_{base_filename}{file_extension}"
    
    # Check if the file already exists
    if UserInput.objects.filter(file=unique_filename).exists():
        # Append a timestamp to ensure uniqueness
        return f"duplicate_files/{username}_{base_filename}_{file_extension}"
    
    # Return the unique filename
    return unique_filename

class UserInput(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    file = models.FileField(upload_to=upload_to, null=True)
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    # def upload_to_gcs(self, filename):
    #     credentials = service_account.Credentials.from_service_account_file(
    #         settings.GOOGLE_APPLICATION_CREDENTIALS,
    #         scopes=['https://www.googleapis.com/auth/cloud-platform'],
    #     )
    #     client = storage.Client(credentials=credentials)
    #     bucket = client.bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET)
    #     blob = bucket.blob(filename)
    #     blob.upload_from_file(self.file)

    # def save(self, *args, **kwargs):
    #     if self.file:
    #         self.upload_to_gcs(self.file.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email

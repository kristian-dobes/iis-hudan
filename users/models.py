from django.db import models

# Create your models here.
class Profile(models.Model):
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    profile_picture_url = models.CharField(max_length=200)
    bio = models.CharField(max_length=1024)
    
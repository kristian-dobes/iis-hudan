from django.db import models

# Create your models here.
class Profile(models.Model):
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    profile_picture_url = models.CharField(max_length=200)
    bio = models.CharField(max_length=1024)
    
    # Visibility choices
    VISIBILITY_CHOICES = [
        (1, 'Visible to everyone'),
        (2, 'Visible to registered users'),
        (3, 'Visible to group members'),
    ]
    # Visibility field
    visibility = models.IntegerField(
        choices=VISIBILITY_CHOICES,
        default=1
    )
    
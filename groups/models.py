from django.db import models
from users.models import Profile

# Create your models here.
class Group(models.Model):
    requested_for_moderator = models.ManyToManyField(Profile, related_name="requested_for_moderator")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=1024)
    moderators = models.ManyToManyField(Profile, related_name="moderators")
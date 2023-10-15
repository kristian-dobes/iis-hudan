from django.db import models
from users.models import Profile

# Create your models here.
class Group(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=1024)
    administrators = models.ManyToManyField(Profile, related_name="administrators")
from django.contrib import admin
from .models import Thread, Post, PostLike

# Register your models here.
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(PostLike)
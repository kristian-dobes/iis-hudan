from django.contrib.sessions.models import Session
from .models import Thread, Post, PostLike
import time
from django.utils import timezone

def thread_get_by_id(request, thread_id):
    try:
        return Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return None
    
def thread_create(request, group, title):
    try:
        thread = Thread.objects.create(group=group, title=title)
        print("Thread created!")
        return thread.id
    except Exception as exception:
        # print exception
        print("Thread not created: %s" % exception)
        return None
    
def post_new(request, user, group, thread, content):
    try:
        post = Post.objects.create(author=user, thread=thread, content=content)
        print("Post created!")
        thread.updated_at = timezone.now()
        thread.save()
        return post.id
    except Exception as exception:
        # print exception
        print("Post not created: %s" % exception)
        return None

def posts_in_thread(request, thread_id):
    try:
        thread = Thread.objects.get(id=thread_id)
        posts = Post.objects.filter(thread=thread).order_by('created_at')
        for post in posts:
            post.likes = PostLike.objects.filter(post=post)
            post.likes_value = 0
            post.likes_up = 0
            post.likes_down = 0
            for like in post.likes:
                post.likes_value += int(like.value)
                if int(like.value) > 0:
                    post.likes_up += 1
                else:
                    post.likes_down += 1
        return posts
    except Exception as exception:
        # print exception
        print("Posts not found: %s" % exception)
        return None

def thread_changed(thread_id, last_changed_time):
    try:
        thread = Thread.objects.get(id=thread_id)
        if thread.updated_at > last_changed_time:
            return True
        else:
            return False
    except Exception as exception:
        # print exception
        print("Thread not found: %s" % exception)
        return None

def post_to_json(post):
    return {
        'id': post.id,
        'author': post.author.username,
        'author_id': post.author.id,
        'author_profile_picture_url': post.author.profile_picture_url,
        'content': post.content,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'likes_value': post.likes_value,
        'likes_up': post.likes_up,
        'likes_down': post.likes_down,
    }

def post_get_by_id(request, post_id):
    try:
        return Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return None

def post_like(request, user, post, value):
    try:
        post_like = PostLike.objects.get(user=user, post=post)
        post_like.value = value
        post_like.save()
        print("Post like updated!")
        post.thread.updated_at = timezone.now()
        post.thread.save()
        return post_like.id
    except PostLike.DoesNotExist:
        try:
            post_like = PostLike.objects.create(user=user, post=post, value=value)
            print("Post like created!")
            post.thread.updated_at = timezone.now()
            post.thread.save()
            return post_like.id
        except Exception as exception:
            # print exception
            print("Post like not created: %s" % exception)
            return None
    except Exception as exception:
        # print exception 
        print("Post like not updated: %s" % exception)
        return None

def post_likes_count(request, post):
    try:
        likes = PostLike.objects.filter(post=post)
        sum = 0
        for like in likes:
            sum += int(like.value)
        return sum
    except Exception as exception:
        # print exception
        print("Post likes not found: %s" % exception)
        return None
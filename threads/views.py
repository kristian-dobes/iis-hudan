from django.shortcuts import render, redirect
from .services import thread_get_by_id, thread_create, post_new, posts_in_thread, post_to_json, thread_changed, post_get_by_id, post_like, post_likes_count, delete_post_service, delete_thread_service, edit_thread_service
from groups.services import group_get_by_id, group_is_user_administrator, group_get_all_members
from users.services import user_current
from .models import Thread
import json
from django.core import serializers
import time
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed

def detail(request, group_id, thread_id):
    thread = thread_get_by_id(request, thread_id)
    group = group_get_by_id(request, group_id)
    user = user_current(request)
    is_group_admin = group_is_user_administrator(request, group_id, user)
    posts = posts_in_thread(request, thread_id)
    print(posts)
    return render(request, 'threads/thread_detail.html', {'thread': thread, 'group': group, 'is_group_admin': is_group_admin, 'posts': posts})

def create(request, group_id):
    group = group_get_by_id(request, group_id)
    user = user_current(request)
    is_group_admin = group_is_user_administrator(request, group_id, user)
    group_members = group_get_all_members(request, group)
    if not is_group_admin and not user.is_admin and not user in group_members:
        print("Is not admin!")
        return redirect('groups:detail', group_id=group_id)
    if request.method == 'POST':
        title = request.POST['name']
        thread_id = thread_create(request, group, title)
        if thread_id is None:
            return redirect('groups:detail', group_id=group_id)
        return redirect('groups:threads:detail', group_id=group_id, thread_id=thread_id)
    else:
        return redirect('groups:detail', group_id=group_id)

def post(request, group_id, thread_id):
    group = group_get_by_id(request, group_id)
    thread = thread_get_by_id(request, thread_id)
    user = user_current(request)
    wait_for_new_post = True
    if request.method == 'POST':
        content = request.POST['content']
        post_new(request, user, group, thread, content)
        wait_for_new_post = False
    
    last_thread_time = thread.updated_at.replace()
    slept = 0
    while not thread_changed(thread_id, last_thread_time) and wait_for_new_post:
        time.sleep(250 / 1000)
        slept += 250 / 1000
        if slept > 10:
            break
    
    posts = posts_in_thread(request, thread_id)
    if posts is None:
        posts = []
    # return json response of posts array
    ret = []
    for post in posts:
        ret.append(post_to_json(post))
    return JsonResponse(ret, safe=False)

def like(request, group_id, thread_id, post_id):
    group = group_get_by_id(request, group_id)
    thread = thread_get_by_id(request, thread_id)
    post = post_get_by_id(request, post_id)
    user = user_current(request)
    if request.method == 'POST':
        value = int(request.POST['value'])
        post_like(request, user, post, value)
    now_likes = post_likes_count(request, post)
    ret = {
        'post_id': post_id,
        'likes': now_likes,
    }
    return JsonResponse(ret, safe=False)


def delete_post(request, group_id, thread_id, post_id):
    # Check if the request is POST
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'], "Only POST method is allowed")

    user = user_current(request)
    group = group_get_by_id(request, group_id)
    thread = thread_get_by_id(request, thread_id)
    post = post_get_by_id(request, post_id)

    if delete_post_service(group, thread, post, user):
        return redirect('groups:threads:detail', group_id=group_id, thread_id=thread_id)
    else:
        return HttpResponseForbidden(json.dumps({"status": "error", "message": "You do not have permission to delete this post"}))
    

def delete_thread(request, thread_id, group_id):
    #group = group_get_by_id(request, group_id)
    thread = thread_get_by_id(request, thread_id)
    delete_thread_service(request, thread)
    return redirect('groups:detail', group_id=group_id)


def edit_thread(request, thread_id, group_id):
   # group = group_get_by_id(request, group_id)
    thread = thread_get_by_id(request, thread_id)
    content = request.POST['title']
    edit_thread_service(request, thread, content)
    return redirect('groups:detail', group_id=group_id)
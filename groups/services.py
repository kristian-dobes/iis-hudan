from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from groups.models import Group
from users.models import Profile
from threads.models import Thread
from users.services import user_current


def group_create(request, name, image_url, description):
    try:
        user = user_current(request)
        if user is None:
            raise Exception('User is not logged in')
        group = Group.objects.create(title=name, image_url=image_url, description=description, owner=user)
        return group.id
    except:
        return None
    
def group_get_by_id(request, group_id):
    try:
        return Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return None

def group_get_all(request):
    try:
        return Group.objects.all()
    except Group.DoesNotExist:
        return None

def group_edit(request, group_id, name, image_url, description, content_visibility):
    try:
        user = user_current(request)
        if user is None:
            raise Exception('User is not logged in')
        group = Group.objects.get(id=group_id)
        if group.owner != user:
            raise Exception('User is not owner of the group')
        group.title = name
        group.image_url = image_url
        group.description = description
        group.content_visibility = content_visibility
        group.save()
        return group.id
    except:
        return None
    
def group_get_threads(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        return Thread.objects.filter(group=group)
    except:
        return None

def group_is_user_administrator(request, group_id, user):
    try:
        group = Group.objects.get(id=group_id)
        return group.moderators.filter(id=user.id).exists() or group.owner == user
    except:
        return False
    
def group_remove(request, group_id):
    print("here?")
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        print("deleted")
        return True
    except Group.DoesNotExist:
        return False

def add_mod_request(request, group_id, user_id):
    print("add_request")
    try:
        print(user_id)
        print(group_id)
        user = Profile.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        group.requested_for_moderator.add(user)
        group.save()
        return True
    except (Profile.DoesNotExist, Group.DoesNotExist):
        return False
    
def add_moderator(request, group_id, user_id):
    try:
        user = Profile.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        group.requested_for_moderator.remove(user)
        group.moderators.add(user)
        group.save()
        return True
    except (Profile.DoesNotExist, Group.DoesNotExist):
        return False
    
def remove_mod_request(request, group_id, user_id):
    try:
        user = Profile.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        group.requested_for_moderator.remove(user)
        group.save()
        return True
    except (Profile.DoesNotExist, Group.DoesNotExist):
        return False
    
def remove_moderator(request, group_id, user_id):
    try:
        user = Profile.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        group.moderators.remove(user)
        group.save()
        return True
    except (Profile.DoesNotExist, Group.DoesNotExist):
        return False
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from .models import Group
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

def group_edit(request, group_id, name, image_url, description):
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
        group.save()
        return group.id
    except:
        return None
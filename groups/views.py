from django.shortcuts import render, redirect
from .services import group_create, group_get_by_id, group_edit, group_get_threads, group_is_user_administrator, group_remove, add_mod_request, remove_mod_request, add_moderator, remove_moderator, add_memb_request, remove_memb_request, add_member, remove_member, add_moderator_username, add_member_username, group_get_all
from users.services import user_current, user_is_logged, user_get_by_id
from threads.services import  thread_get_by_id
from .models import Group
from users.models import Profile

# Create your views here.
def detail(request, group_id):
    user = user_current(request)
    group = group_get_by_id(request, group_id)
    threads = group_get_threads(request, group_id)
    is_user_admin = group_is_user_administrator(request, group_id, user) 
    is_user_logged = user_is_logged(request)
    return render(request, 'groups/group_detail.html', {'group': group, 'threads': threads, 'is_user_admin': is_user_admin, 'is_user_logged': is_user_logged})

def edit(request, group_id):
    if request.method == 'POST':
        name = request.POST['name']
        image_url = request.POST['image_url']
        description = request.POST['description']
        content_visibility = request.POST['content_visibility']
        delete_group = request.POST.get('delete_group', False)
        if delete_group:
            group_remove(request, group_id)
            return redirect('home')
        
        edited_id = group_edit(request, group_id, name, image_url, description, content_visibility)
        if edited_id is None:
        # show group detail with error message
            group = group_get_by_id(request, group_id)
            return render(request, 'groups/edit_group.html', {'group': group, 'error': 'Error during group edit'})
        else:
            return redirect('groups:detail', group_id=edited_id)
    
    group = group_get_by_id(request, group_id)
    user = user_current(request)
    
    #is_user_admin = group_is_user_administrator(request, group_id, user_current(request))
    #if group == None or (group.owner != user and not is_user_admin):
    if group == None or (group.owner != user and not user.is_admin):
        return redirect('groups:detail', group_id=group_id)
    return render(request, 'groups/edit_group.html', {'group': group})

def create(request):
    if user_current(request) is None:
        return redirect('users:login')
    if request.method == 'POST':
        name = request.POST['name']
        image_url = request.POST['image_url']
        description = request.POST['description']
        visibility = request.POST['content_visibility']
        created_id = group_create(request, name, image_url, description, visibility)
        if created_id is None:
            return render(request, 'groups/create_group.html', {'error': 'Error during group creation'})
        else:
            return redirect('groups:detail', group_id=created_id)
            
    return render(request, 'groups/create_group.html')


def list_groups(request):
    search_query = request.GET.get('search', '')
    if search_query:
        groups = Group.objects.filter(username__icontains=search_query)
    else:
        groups = group_get_all(request)

    return render(request, 'groups/list_groups.html', {'groups': groups, 'request': request})


def delete_group(request, group_id):
    group = group_get_by_id(request, group_id)
    if request.method == "POST":
        group_remove(request, group.id)  
        groups = group_get_all(request)
        return render(request, 'groups/list_groups.html', {'groups': groups})
    return render(request, 'groups/confirm_delete.html', {'group': group})


def add_moderator_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    add_mod_request(request, group.id, user.id)
    return detail(request, group_id)


def approve_moderator_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    add_moderator(request, group.id, user.id)
    return detail(request, group_id)

def reject_moderator_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    remove_mod_request(request, group.id, user.id)
    return detail(request, group_id)


def delete_moderator(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    remove_moderator(request, group.id, user.id)
    return detail(request, group_id)

# Members
def add_member_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    add_memb_request(request, group.id, user.id)
    return detail(request, group_id)

def approve_member_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    add_member(request, group.id, user.id)
    return detail(request, group_id)

def reject_member_request(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    remove_memb_request(request, group.id, user.id)
    return detail(request, group_id)

def delete_member(request, group_id, user_id):
    group = group_get_by_id(request, group_id)
    user = user_get_by_id(request, user_id)
    remove_member(request, group.id, user.id)
    return detail(request, group_id)

def new_member(request, group_id):
    user = user_current(request)
    group = group_get_by_id(request, group_id)
    username =  request.POST['new_member']
    threads = group_get_threads(request, group_id)
    is_user_admin = group_is_user_administrator(request, group_id, user) 
    is_user_logged = user_is_logged(request)
    if not add_member_username(request, group.id, username):
            return render(request, 'groups/group_detail.html', {'group': group, 'threads': threads, 'is_user_admin': is_user_admin, 'is_user_logged': is_user_logged,'error_mem': 'Error during user search'})
    return render(request, 'groups/group_detail.html', {'group': group, 'threads': threads, 'is_user_admin': is_user_admin, 'is_user_logged': is_user_logged})

def new_mod(request, group_id):
    user = user_current(request)
    group = group_get_by_id(request, group_id)
    username =  request.POST['new_mod']
    threads = group_get_threads(request, group_id)
    is_user_admin = group_is_user_administrator(request, group_id, user) 
    is_user_logged = user_is_logged(request)
    add_moderator_username(request, group.id, username)

    if not group.members.filter(username=username).exists():
        if not add_member_username(request, group.id, username):
            return render(request, 'groups/group_detail.html', {'group': group, 'threads': threads, 'is_user_admin': is_user_admin, 'is_user_logged': is_user_logged, 'error_mod': 'Error during user search'})
    return render(request, 'groups/group_detail.html', {'group': group, 'threads': threads, 'is_user_admin': is_user_admin, 'is_user_logged': is_user_logged})


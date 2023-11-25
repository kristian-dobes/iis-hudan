from django.shortcuts import render, redirect
from .services import group_create, group_get_by_id, group_edit, group_get_threads, group_is_user_administrator, group_remove, add_mod_request, remove_mod_request, add_moderator, remove_moderator
from users.services import user_current, user_is_logged, user_get_by_id
from .models import Group

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
        edited_id = group_edit(request, group_id, name, image_url, description, content_visibility)
        if edited_id is None:
        # show group detail with error message
            group = group_get_by_id(request, group_id)
            return render(request, 'groups/edit_group.html', {'group': group, 'error': 'Chyba při editaci skupiny'})
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
        created_id = group_create(request, name, image_url, description)
        if created_id is None:
            return render(request, 'groups/create_group.html', {'error': 'Chyba při vytváření skupiny'})
        else:
            return redirect('groups:detail', group_id=created_id)
            
    return render(request, 'groups/create_group.html')


def list_groups(request):
    print("Listing groups")
    search_query = request.GET.get('search', '')
    if search_query:
        print("query")
        # Adjust the filter to match the attributes of your Profile model
        groups = Group.objects.filter(username__icontains=search_query)
    else:
        print("gg")
        groups = Group.objects.all()
    print("here?")

    return render(request, 'groups/list_groups.html', {'groups': groups, 'request': request})


def delete_group(request, group_id):
    group = group_get_by_id(request, group_id)
    if request.method == "POST":
        group_remove(request, group.id)  # This will delete the User and the associated Profile
        groups = Group.objects.all()
        return render(request, 'groups/list_groups.html', {'groups': groups})
    print("confirm")
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
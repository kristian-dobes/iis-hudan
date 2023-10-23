from django.shortcuts import render, redirect
from .services import group_create, group_get_by_id, group_edit
from users.services import user_current

# Create your views here.
def detail(request, group_id):
    group = group_get_by_id(request, group_id)
    return render(request, 'groups/group_detail.html', {'group': group})

def edit(request, group_id):
    if request.method == 'POST':
        name = request.POST['name']
        image_url = request.POST['image_url']
        description = request.POST['description']
        edited_id = group_edit(request, group_id, name, image_url, description)
        if edited_id is None:
        # show group detail with error message
            group = group_get_by_id(request, group_id)
            return render(request, 'groups/edit_group.html', {'group': group, 'error': 'Chyba při editaci skupiny'})
        else:
            return redirect('groups:detail', group_id=edited_id)
    
    group = group_get_by_id(request, group_id)
    user = user_current(request)
    if group == None or group.owner != user:
        return redirect('groups:detail', group_id=group_id)
    return render(request, 'groups/edit_group.html', {'group': group})

def create(request):
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
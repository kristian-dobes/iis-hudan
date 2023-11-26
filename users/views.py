from django.shortcuts import render, redirect
from .models import Profile
from .services import user_get_by_id, user_remove, user_is_logged, user_logout, verify_password, user_current, change_password_service, profile_get_all
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from groups.services import common_group

def detail(request, user_id):
    user = user_get_by_id(request, user_id)
    is_user_logged = user_is_logged(request)
    
    if not is_user_logged:
        return render(request, 'users/user_detail.html', {'profile': user, 'is_user_logged': is_user_logged})
    
    current_user = user_current(request)
    any_common_group = common_group(request, user_id, current_user.id)
    return render(request, 'users/user_detail.html', {'profile': user, 'is_user_logged': is_user_logged, 'common_group': any_common_group})

def edit(request, user_id):
    print(user_id)
    if request.method == 'POST':
        user = user_get_by_id(request, user_id)
        user.username = request.POST['username']
        user.profile_picture_url = request.POST['image_url']
        user.bio = request.POST['bio']
        user.visibility = request.POST['visibility']
        
        user.save()
        return redirect('users:detail', user_id=user.id )
    else:
        user = user_get_by_id(request, user_id)
        return render(request, 'users/edit_user.html', {'profile': user})

def list_users(request):
    search_query = request.GET.get('search', '')
    if search_query:
        # Adjust the filter to match the attributes of your Profile model
        profiles = Profile.objects.filter(username__icontains=search_query) # TODO move to services
    else:
        profiles = profile_get_all(request)

    return render(request, 'users/all_users.html', {'profiles': profiles, 'request': request})

def delete_self(request, user_id):
    profile = user_get_by_id(request, user_id)
    if request.method == "POST":
        user_remove(request, profile.id)  # This will delete the User and the associated Profile
        user_logout(request)
        return redirect('home')
    form_action = reverse('users:delete_self', kwargs={'user_id': user_id})
    return render(request, 'users/confirm_delete.html', {'form_action': form_action})

def delete_user(request, user_id):
    profile = user_get_by_id(request, user_id)
    if request.method == "POST":
        user_remove(request, profile.id)  # This will delete the User and the associated Profile
        profiles = Profile.objects.all()
        return render(request, 'users/all_users.html', {'profiles': profiles})
    cur_user = user_get_by_id(request, request.session['user_id'])
    if user_id != cur_user.id:
        form_action = reverse('users:delete_user', kwargs={'user_id': user_id})
    else:
        form_action = reverse('users:delete_self', kwargs={'user_id': user_id})
    return render(request, 'users/confirm_delete.html', {'form_action': form_action})

def change_password(request, user_id):
    if request.method == 'POST':
        user = user_get_by_id(request, request.session['user_id'])
        cur_user = user_get_by_id(request, request.session['user_id'])

        password = request.POST['password']
        password2 = request.POST['password2']
        if cur_user.is_admin:
            change_password_service(request, password, password2, user_id)
            profiles = profile_get_all(request)
            return render(request, 'users/all_users.html', {'profiles': profiles})
        
        if verify_password(request.POST['old_password'], user.password):
            change_password_service(request, password, password2, user_id)
            return redirect('users:detail', user_id=user.id)
        else:
            return render(request, 'users/change_password.html', {'error': 'Wrong password!'})
    else:
        return render(request, 'users/change_password.html')


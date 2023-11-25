from django.shortcuts import render, redirect
from .models import Profile
from .services import user_get_by_id, user_remove, user_is_logged
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .services import user_get_by_id, verify_password

def detail(request, user_id):
    user = user_get_by_id(request, user_id)
    is_user_logged = user_is_logged(request)
    
    return render(request, 'users/user_detail.html', {'profile': user, 'is_user_logged': is_user_logged})

def edit(request, user_id):
    print(user_id)
    if request.method == 'POST':
        user = user_get_by_id(request, request.session['user_id'])
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
        profiles = Profile.objects.filter(username__icontains=search_query)
    else:
        profiles = Profile.objects.all()

    return render(request, 'users/all_users.html', {'profiles': profiles, 'request': request})


def delete_user(request, user_id):
    profile = user_get_by_id(request, user_id)
    if request.method == "POST":
        user_remove(request, profile.id)  # This will delete the User and the associated Profile
        profiles = Profile.objects.all()
        return render(request, 'users/all_users.html', {'profiles': profiles})
    return render(request, 'users/confirm_delete.html', {'profile': profile})

    
def change_password(request, user_id):
    if request.method == 'POST':
        user = user_get_by_id(request, request.session['user_id'])
        # TODO doesnt work, needs adjustments, needs to be hashed? 
        if verify_password(user.password, request.POST['old_password']):
            user.password = request.POST['password']
            user.save()
            return redirect('users:detail', user_id=user.id)
        else:
            return render(request, 'users/change_password.html', {'error': 'Špatné heslo'})
    else:
        return render(request, 'users/change_password.html')

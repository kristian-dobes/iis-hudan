from django.shortcuts import render, redirect
from .models import Profile
from .services import user_get_by_id, verify_password

def detail(request, user_id):
    user = user_get_by_id(request, user_id)
    return render(request, 'users/user_detail.html', {'profile': user})

def edit(request, user_id):
    if request.method == 'POST':
        user = user_get_by_id(request, request.session['user_id'])
        user.username = request.POST['username']
        user.profile_picture_url = request.POST['image_url']
        user.bio = request.POST['bio']
        user.save()
        return redirect('users:detail', user_id=user.id)
    else:
        return render(request, 'users/edit_user.html')
    
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
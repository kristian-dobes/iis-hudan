from django.shortcuts import render, redirect
from .models import Profile
from .services import user_get_by_id

def detail(request, user_id):
    user = user_get_by_id(request, user_id)
    return render(request, 'users/user_detail.html', {'profile': user})

def edit(request):
    if request.method == 'POST':
        user = user_get_by_id(request, request.session['user_id'])
        user.username = request.POST['username']
        user.save()
        return redirect('detail', user_id=user.id)
    else:
        return render(request, 'users/edit.html')
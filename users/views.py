from django.shortcuts import render, redirect
from .models import Profile
from .services import user_get_by_id, user_remove
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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
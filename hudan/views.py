from django.shortcuts import render, redirect
from users.services import user_register, user_login, user_logout, user_is_logged, user_current
from groups.services import group_get_all
from users.models import Profile

# Create your views here.
def register(request):
    if user_is_logged(request):
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if user_register(request, username, password, password2):
            return redirect('home')
        else:
            return render(request, 'register.html', {'error': 'Username is already taken'})
    
    return render(request, 'register.html')

def login(request):
    if user_is_logged(request):
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if user_login(request, username, password):
            print("Logged in.")
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def logout(request):
    user_logout(request)
    return redirect('home')

def home(request):
    print("Redirected to home!")
    groups = group_get_all(request)
    print("Got all groups.")
    visible_groups = 0
    for group in groups:
        # if not current_user and group.content_visibility > 1
        if group.content_visibility > 1:
            if not user_is_logged(request):
                continue
        visible_groups += 1
    print("Visible groups: " + str(visible_groups))
    return render(request, 'home.html', {'groups': groups, 'visible_groups': visible_groups})
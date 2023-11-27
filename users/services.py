from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from .models import Profile

def hash_password(raw_password):
    return make_password(raw_password)

def verify_password(raw_password, hashed_password):
    return check_password(raw_password, hashed_password)

def user_register(request, username, password, password2):
    try: 
        user = Profile.objects.get(username=username)
        return False
    except Profile.DoesNotExist:
        if password != password2:
            return False
        else:
            user = Profile.objects.create(username=username, password=hash_password(password))
            request.session['user_id'] = user.id
            return True

def user_login(request, username, password):
    try:
        user = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return False

    # Check if the provided password matches the hash stored in the database
    if verify_password(password, user.password):
        # Use Django's sessions
        request.session['user_id'] = user.id
        return True
    
    return False

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

def user_is_logged(request):
    return 'user_id' in request.session

def user_current(request):
    if user_is_logged(request):
        return Profile.objects.get(id=request.session['user_id'])
    else:
        return None
    
def user_get_by_id(request, user_id):
    try:
        return Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
        return None
    
def user_remove(request, user_id):
    print("here?")
    try:
        user = Profile.objects.get(id=user_id)
        user.delete()
        print("deleted")
        return True
    except Profile.DoesNotExist:
        return False
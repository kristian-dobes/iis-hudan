from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
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

def user_edit(request, user_id, username, profile_picture_url, bio, visibility):
    try:
        user = Profile.objects.get(id=user_id)
        curr_user = user_current(request)
        if curr_user is None:
            raise Exception('User is not logged in')
        if user != curr_user and not curr_user.is_admin:
            raise Exception('User does not have permission to edit this profile')
        user.username = username
        
        # Validate profile_picture_url if it is not empty
        if profile_picture_url:
            validate = URLValidator()
            try:
                validate(profile_picture_url)
            except ValidationError as e:
                raise Exception('Invalid image URL')
        
        user.profile_picture_url = profile_picture_url
        user.bio = bio
        user.visibility = visibility
        user.save()
        return True
    except Profile.DoesNotExist:
        return False
    except Exception as e:
        return False

def profile_get_all(request):
    try:
        return Profile.objects.all()
    except Profile.DoesNotExist:
        return None


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


def change_password_service(request, password, password2, user_id):
    try: 
        user = Profile.objects.get(id=user_id)
        if password != password2:
            return False
        else:
            print(password)
            user.password=hash_password(password)
            user.save()
            return True
    except Profile.DoesNotExist:
        return False
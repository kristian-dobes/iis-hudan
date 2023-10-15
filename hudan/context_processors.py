from users.services import user_current

def user_current_context(request):
    current_user = user_current(request)
    return {'current_user': current_user}

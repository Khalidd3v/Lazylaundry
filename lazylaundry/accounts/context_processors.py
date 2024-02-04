

def user_data(request):
    user = request.user if request.user.is_authenticated else None
    return {'user_get': user}
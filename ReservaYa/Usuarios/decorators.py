from django.http import HttpResponseForbidden
from functools import wraps

def restaurant_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Acceso denegado: necesitas iniciar sesión.")
        if not request.user.is_restaurant:
            return HttpResponseForbidden("Acceso denegado: necesitas ser administrador de restaurante.")
        return view_func(request, *args, **kwargs)
    return wrapper

from django.http import HttpResponseForbidden

def restaurant_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_restaurant_admin():
            return HttpResponseForbidden("Acceso denegado: necesitas ser administrador de restaurante.")
        return view_func(request, *args, **kwargs)
    return wrapper

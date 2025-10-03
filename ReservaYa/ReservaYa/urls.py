from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Usuarios.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), 

    # URLs de la app Usuarios
    path('usuarios/', include('Usuarios.urls', namespace='usuarios')),

    # URLs de django-allauth (Google login, registro social)
    path('accounts/', include('allauth.urls')),

    # Otras apps, si las tuviera
    # path('restaurantes/', include('Restaurantes.urls', namespace='restaurantes')),
=======
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservas/', include('Reservas.urls')),
>>>>>>> Reservas
]

# Servir archivos media durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Usuarios.views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'), 

    path('restaurantes/', include('Restaurantes.urls', namespace='restaurantes')), 
    path('usuarios/', include('Usuarios.urls', namespace='usuarios')),
    path('accounts/', include('allauth.urls')),
    path('reservas/', include('Reservas.urls')),
]

# Servir archivos media durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

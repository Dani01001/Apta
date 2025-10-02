from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ('telefono', 'role', 'perfil_imagen')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
    (None, {'fields': ('telefono', 'role', 'perfil_imagen')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser


Usuario = get_user_model()

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    telefono = forms.CharField(label='Teléfono', required=False)
    perfil_imagen = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'telefono', 'perfil_imagen', 'password1', 'password2')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'telefono', 'perfil_imagen')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo o usuario")
    password = forms.CharField(widget=forms.PasswordInput)

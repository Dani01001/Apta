from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import restaurant_admin_required
from Restaurantes.models import Restaurante

Usuario = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=user.username, password=form.cleaned_data["password1"])
            if user is not None:
                login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a ReservaYa.")
            return redirect("usuarios:profile")
    else:
        form = RegisterForm()
    return render(request, "usuarios/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_restaurant:
                return redirect("usuarios:dashboard_restaurante")
            else:
                return redirect("usuarios:dashboard_usuario")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, "usuarios/login.html")
    return render(request, "usuarios/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("home")

@login_required
def profile_view(request):
    return render(request, "usuarios/profile.html")

@login_required
def profile_edit_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect("usuarios:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "usuarios/profile_edit.html", {"form": form})

def home_view(request):
    restaurantes = Restaurante.objects.filter(activo=True)
    for r in restaurantes:
        try:
            r.estrellas = int(round(getattr(r, 'rating', 4.5)))
        except:
            r.estrellas = 0
    return render(request, "home.html", {"restaurantes": restaurantes})

@login_required
def dashboard(request):
    if request.user.is_restaurant:
        return render(request, "usuarios/dashboard_restaurante.html")
    else:
        return render(request, "usuarios/dashboard_usuario.html")

@restaurant_admin_required
def panel_restaurante(request):
    return render(request, "usuarios/dashboard_restaurante.html")

def quienes_somos(request):
    return render(request, "quienes_somos.html")

def terminos(request):
    return render(request, "terminos.html")

def privacidad(request):
    return render(request, "privacidad.html")

def contacto(request):
    return render(request, "contacto.html")

def paginapriv(request):
    return render(request, "usuarios/paginapriv.html")

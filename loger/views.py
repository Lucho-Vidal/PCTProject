from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required  , user_passes_test
from django.contrib.auth.models import User, Group
from .forms import SignupForm

def in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

# Create your views here.
def signIn(request):
    if request.method == "GET":
        return render(request, "loger/signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "loger/signin.html", {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
@user_passes_test(in_group("jefatura"))
def signup(request):
    error = None
    if request.method == "POST":
        form = SignupForm(request.POST, user=request.user)
        if form.is_valid():
            username = form.cleaned_data["username"]
            group = form.cleaned_data["group"]

            if User.objects.filter(username=username).exists():
                error = "El usuario ya existe"
            else:
                user = User.objects.create_user(
                    username=username,
                    password="Inicio1"  # contraseña por defecto
                )
                user.groups.add(group)
                return redirect("home")
    else:
        form = SignupForm(user=request.user)

    return render(request, "loger/signup.html", {"form": form, "error": error})


def signOut(request):
    logout(request)
    return redirect('home')

@login_required
def home(request):
    titulo = "Página de inicio"
    mensaje = "Bienvenido invitado"
    roles = []

    if request.user.is_authenticated:
        roles = list(request.user.groups.values_list("name", flat=True))
        if "administrador" in roles:
            titulo = "Bienvenido, tu usuario es Administrador"
            mensaje = "Tienes todos los permisos"
        elif "jefatura" in roles:
            titulo = "Bienvenido, tu usuario tiene rango de Jefatura"
            mensaje = "Tienes permisos elevados"
        elif "supervisor" in roles:
            titulo = "Bienvenido, tu usuario es Supervisor"
            mensaje = "Tienes permisos de supervisión"
        elif "visor" in roles:
            titulo = "Bienvenido, tu usuario es Visor"
            mensaje = "Tienes permisos de solo lectura"
        else:
            titulo = "Bienvenido, tu usuario no tiene rol asignado"
            mensaje = "Por favor, contacta con el administrador."

    return render(request, "loger/home.html", {"titulo":titulo,"mensaje": mensaje, "roles": roles})
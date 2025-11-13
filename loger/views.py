from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.
def signIn(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')
        
def signUp(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe!"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm,
             "error": "Las contraseñas no coinciden"},
        )

def signOut(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, "home.html")

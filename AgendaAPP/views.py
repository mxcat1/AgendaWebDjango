from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'pages/login.html', {'titlepage': 'Login', 'tipopagina': 'login-page'})


def registro(request):
    return render(request, 'pages/registro.html', {'titlepage': 'Registro', 'tipopagina': 'sidebar-mini'})


def perfil(request):
    return render(request, 'pages/perfil.html', {'titlepage': 'Mi Perfil', 'tipopagina': 'sidebar-mini'})


def contactos(request):
    return render(request, 'pages/contactos.html', {'titlepage': 'Mis Contactos', 'tipopagina': 'sidebar-mini'})


def grupocontactos(request):
    return render(request, 'pages/grupocontactos.html',
                  {'titlepage': 'Mis Grupos de Contactos', 'tipopagina': 'sidebar-mini'})

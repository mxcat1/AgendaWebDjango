from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'pages/login.html', {'titlepage': 'Login', 'tipopagina': 'login-page'})


def perfil(request):
    return render(request, 'pages/perfil.html', {'titlepage': 'Mi Perfil', 'tipopagina': 'sidebar-mini'})

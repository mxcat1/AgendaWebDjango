"""AgendaWebDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from AgendaAPP import views as AgendaAPPVistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AgendaAPPVistas.index, name='index'),
    path('login/', AgendaAPPVistas.login, name='login'),
    path('logout/', AgendaAPPVistas.logout, name='cerrarsession'),
    path('registro/', AgendaAPPVistas.registro, name='registro'),
    path('registrousuario/<str:Codigo>', AgendaAPPVistas.registrousuario, name='registrousuario'),
    path('cambiarpassword/', AgendaAPPVistas.cambiarcontra, name='cambiarpassword'),
    path('restablecer_password/',
         auth_views.PasswordResetView.as_view(template_name='pages/reset_password/password_reset_form.html'),
         name='password_reset'),
    path('restablecer-password/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='pages/reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('restablecer-password-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='pages/reset_password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('restablecer-password-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pages/reset_password/password_reset_complete.html'), name='password_reset_complete'),
    path('perfil/<int:iduser>', AgendaAPPVistas.editarDatosUsuario, name='perfil'),
    # path('perfil/<int:iduser>', AgendaAPPVistas.editarDatosUsuario.as_view(template_variables={'titlepage': 'Mi Perfil', 'tipopagina': 'sidebar-mini'}), name='perfil'),
    # path('contactos/', AgendaAPPVistas.ContactoCreateView.as_view(template_variables={'titlepage': 'Mis Contactos', 'tipopagina': 'sidebar-mini'}), name='contactos'),
    path('contactos/', AgendaAPPVistas.contactos, name='contactos'),
    path('contacto/nuevo/<str:personaid>', AgendaAPPVistas.contactopersonagrupo, name='contactos-nuevo'),
    path('contacto/datos/<str:contactoid>', AgendaAPPVistas.contactodatos, name='contacto-datos'),
    path('contacto/mensaje/whatsapp', AgendaAPPVistas.mensajewsp, name='msj-whatsapp'),
    path('telefono/nueva/<str:personaid>', AgendaAPPVistas.telefononuevo, name='new-telefono'),
    path('telefono/editar/<str:telefonoid>', AgendaAPPVistas.telefonoeditar, name='edit-telefono'),
    path('telefono/eliminar/<str:telefonoid>', AgendaAPPVistas.telefonoeliminar, name='delete-telefono'),
    path('correo/nueva/<str:personaid>', AgendaAPPVistas.correonuevo, name='new-correo'),
    path('direccion/nueva/<str:personaid>', AgendaAPPVistas.direccionnueva, name='new-direction'),
    path('grupocontactos/', AgendaAPPVistas.grupocontactos, name='grupocontactos'),
    path('grupocontactos/editar/<int:idgrupocontacto>', AgendaAPPVistas.grupocontactoseditar,
         name='grupocontactoseditar'),
    path('grupocontactos/eliminar/<int:idgrupocontacto>', AgendaAPPVistas.grupocontactoeliminar,
         name='grupocontactoseliminar'),
]
# Configuracion para ver Imagenes
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

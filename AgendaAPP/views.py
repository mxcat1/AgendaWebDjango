from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import logout as cerrarsession, update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from shapeshifter.views import MultiModelFormView, MultiFormView
from shapeshifter.mixins import MultiSuccessMessageMixin

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *

# Otras app
import pywhatkit
from datetime import datetime


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        usuario = Usuario.objects.get(id=request.user.id)
        return render(request, 'pages/index.html',
                      {'titlepage': 'Inicio', 'tipopagina': 'sidebar-mini layout-fixed', 'user': usuario})
    return redirect('/login')


def login(request):
    form = UsuarioAuthenticationForm()
    if request.method == 'POST':
        form = UsuarioAuthenticationForm(request.POST)
        nombreusuario = request.POST['username']
        contrasenia = request.POST['password']

        user = authenticate(username=nombreusuario, password=contrasenia)

        if user is not None:
            do_login(request, user)
            return redirect('/')
    return render(request, 'pages/login.html', {'titlepage': 'Login', 'tipopagina': 'login-page', 'form': form,
                                                'message': 'Error no se pudo logear'})


def logout(request):
    cerrarsession(request)
    return redirect('/')


# Registro de la tabla persona de la base de datos
def registro(request):
    form = PersonaCreateForm()
    if request.method == 'POST':
        form = PersonaCreateForm(request.POST, request.FILES)
        if form.is_valid():
            persona = form.save(commit=False)
            persona.save()
            codigo = persona.id
            return redirect(f'/registrousuario/{str(codigo)}')

    return render(request, 'pages/registro.html', {'titlepage': 'Registro', 'tipopagina': 'login-page', 'form': form})


# Registros d ela tabla usuarios
def registrousuario(request, Codigo):
    if Codigo is not None:
        form = UsuarioUserCreationFormInvitado()
        if request.method == 'POST':
            form = UsuarioUserCreationFormInvitado(request.POST)
            if form.is_valid():
                usuarionuevo = form.save(commit=False)
                usuarionuevo.save()
                return redirect('/login')
        return render(request, 'pages/registrousuario.html',
                      {'titlepage': 'Registro', 'tipopagina': 'login-page', 'form': form, 'codigo': Codigo})
    else:
        return render('/registro')


# def perfil(request):
#     return render(request, 'pages/perfil.html', {'titlepage': 'Mi Perfil', 'tipopagina': 'sidebar-mini'})
# Editar datos d ela tabla persona
def editarDatosUsuario(request, iduser):
    if request.user.is_authenticated:
        userid = request.user.id
        usuario = Usuario.objects.get(id=userid)
        personadatos = Persona.objects.get(id=usuario.codPersona.id)
        formupdate = PersonaUpdateForm(instance=personadatos)
        if request.method == 'POST':
            formupdate = PersonaUpdateForm(request.POST, request.FILES, instance=personadatos)
            if formupdate.is_valid():
                usuarioactualizar = formupdate.save(commit=False)
                usuarioactualizar.save()
                messages.success(request, 'Datos del Perfil de Usuario guardados correctamente')

        return render(request, 'pages/perfil.html',
                      {'titlepage': 'Mi Perfil', 'tipopagina': 'sidebar-mini', 'form': formupdate, 'userid': iduser,
                       'user': usuario})
    return redirect('/login')


# Editar contraseña de la tabla usuario
def cambiarcontra(request):
    if request.user.is_authenticated:
        formchangepass = PasswordChangeForm(request.user)
        if request.method == 'POST':
            formchangepass = PasswordChangeForm(request.user, request.POST)
            if formchangepass.is_valid():
                passchange = formchangepass.save(commit=False)
                passchange.save()
                update_session_auth_hash(request, passchange)
                messages.success(request, 'Contraseña Cambiada con Exito')
                return redirect('/')
            else:
                messages.error(request, 'Error contraseña incorrecta')
        return render(request, 'pages/cambiarpassword.html',
                      {'titlepage': 'Cambiar Contraseña', 'tipopagina': 'sidebar-mini', 'form': formchangepass})
    else:
        return redirect('/login')


# class editarDatosUsuario(LoginRequiredMixin, MultiModelFormView, MultiSuccessMessageMixin):
#     form_classes = (UsuarioUpdateForm, PersonaUpdateForm)
#     template_name = 'pages/perfil.html'
#     success_url = reverse_lazy('index')
#     success_message = 'Los datos de tu Perfil fueron actualizados'
#     template_variables = None
#
#     def get_instances(self):
#         persona_instance = Persona.objects.filter(id=self.request.user.codPersona.id).first()
#         instances = {'usuarioupdateform': self.request.user,
#                      'personaupdateform': persona_instance, }
#         return instances
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(self.template_variables)
#         return context


def contactos(request):
    if request.user.is_authenticated:
        formcontactopersona = PersonaCreateContactForm()
        grupocontactoslista = GrupoContactos.objects.filter(codUsuario=request.user.id)
        contactoslista = ContactoGrupoContactos.objects.filter(codGrupo__in=grupocontactoslista)
        telefonoscontactoslista = TelefonoPersona.objects.all()
        if request.method == 'POST':
            formcontactopersonacreate = PersonaCreateContactForm(request.POST, request.FILES)
            if formcontactopersonacreate.is_valid():
                personacontactcreate = formcontactopersonacreate.save(commit=False)
                personacontactcreate.save()
                messages.success(request,
                                 'Contacto Creado Sadisfactoriamente Elija el grupo Contacto al que Pertenecera')
                return redirect(f'/contacto/nuevo/{str(personacontactcreate.id)}')
            else:
                messages.error(request, 'No se pudo guardar el nuevo Contacto')
        return render(request, 'pages/contactos.html',
                      {'titlepage': 'Mis Contactos', 'tipopagina'
                      : 'sidebar-mini', 'form': formcontactopersona,
                       'contactos': contactoslista, 'telefonoslistas': telefonoscontactoslista})
    else:
        return redirect('/login')


def contactopersonagrupo(request, personaid):
    if request.user.is_authenticated:
        formcontactogrupo = ContactoGrupoContactoAddForm(request.user.id)
        if request.method == 'POST':
            personacontactonew = Persona.objects.get(id=personaid)
            contactonuevo = Contacto(codPersona=personacontactonew)
            contactonuevo.save()
            request.POST._mutable = True
            request.POST['codContacto'] = str(contactonuevo.id)
            request.POST._mutable = False
            formcontactogrupo = ContactoGrupoContactoAddForm(request.user.id, request.POST)
            if formcontactogrupo.is_valid():
                nuevocontactogrupo = formcontactogrupo.save(commit=False)
                nuevocontactogrupo.save()
                messages.success(request, 'Nuevo Contacto Agregado con exito')
                return redirect('contactos')
            else:
                messages.error(request, 'Error no se pudo guardar el Contacto')
        return render(request, 'pages/contactonuevo.html',
                      {'titlepage': 'Nuevo Contacto', 'tipopagina': 'sidebar-mini', 'form': formcontactogrupo})
    else:
        return redirect('/login')


def contactodatos(request, contactoid):
    if request.user.is_authenticated:
        contactopersonadatos = Contacto.objects.get(id=contactoid)
        telefonos = TelefonoPersona.objects.filter(codPersona=contactopersonadatos.codPersona)
        correos = CorreoPersona.objects.filter(codPersona=contactopersonadatos.codPersona)
        direcciones = DireccionPersona.objects.filter(codPersona=contactopersonadatos.codPersona)
        formcontactodatos = PersonaUpdateForm(instance=contactopersonadatos.codPersona)
        if request.method == 'POST':
            formcontactodatos = PersonaUpdateForm(request.POST, request.FILES, instance=contactopersonadatos.codPersona)
            if formcontactodatos.is_valid():
                editarcontacto = formcontactodatos.save(commit=False)
                editarcontacto.save()
                messages.success(request, 'Contacto Editado correctamente')
                return redirect('contactos')
            else:
                messages.error(request, 'No se pudo editar el contacto')

        return render(request, 'pages/contacto-datos.html',
                      {'titlepage': 'Contacto Datos', 'tipopagina': 'sidebar-mini',
                       'contactodatos': contactopersonadatos, 'telefonoscontacto': telefonos,
                       'correoscontacto': correos,
                       'direccionescontacto': direcciones,
                       'form': formcontactodatos})

    else:
        return redirect('/login')


# Mensaje por Whatsapp todavia en prueba
def mensajewsp(request):
    try:
        tiempo = datetime.now()
        pywhatkit.sendwhatmsg('+51987323795', 'Prueba mensaje', tiempo.hour, tiempo.minute + 1)
        print('Mensaje Enviado')
        return redirect('contactos')

    except:
        print('Error')
        return redirect('contactos')


# class ContactoCreateView(MultiFormView):
#     form_classes = (PersonaCreateContactForm, ContactoCreateForm, ContactoGrupoContactoAddForm)
#     template_name = 'pages/contactos.html'
#     success_url = reverse_lazy('contactos')
#     template_variables = None
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(self.template_variables)
#         return context


def grupocontactos(request):
    if request.user.is_authenticated:
        formcreategroup = GrupoContactoCreateForm()
        gruposcontactoslista = GrupoContactos.objects.filter(codUsuario=request.user.id)
        if request.method == 'POST':
            request.POST._mutable = True
            request.POST['codUsuario'] = str(request.user.id)
            request.POST._mutable = False
            formcreategroup = GrupoContactoCreateForm(request.POST)
            if formcreategroup.is_valid():
                groupcontact = formcreategroup.save(commit=False)
                groupcontact.save()
                messages.success(request, 'Grupo de Contactos Creado exitosamente')
                return redirect('/grupocontactos')
            else:
                messages.error(request, 'Error no se pudo guardar el grupo correctamente')

        return render(request, 'pages/grupocontactos.html',
                      {'titlepage': 'Mis Grupos de Contactos', 'tipopagina': 'sidebar-mini',
                       'grupocontactos': gruposcontactoslista, 'form': formcreategroup})
    else:
        return redirect('/login')


def grupocontactoseditar(request, idgrupocontacto):
    if request.user.is_authenticated:
        grupocontactoedit = GrupoContactos.objects.get(id=idgrupocontacto)
        formeditgroup = GrupoContactoEditForm(instance=grupocontactoedit)

        if request.method == 'POST':
            formeditgroup = GrupoContactoEditForm(request.POST, instance=grupocontactoedit)
            if formeditgroup.is_valid():
                grupocontactoeditado = formeditgroup.save(commit=False)
                grupocontactoeditado.save()
                messages.success(request, 'Datos del Grupo de Contacto del Usuario editado correctamente')
                return redirect('/grupocontactos')
            else:
                messages.error(request, 'Error al editar el grupo contacto seleccionado')
        else:
            return render(request, 'pages/grupocontactoedit.html',
                          {'titlepage': 'Editar Nombre del Grupo Contacto', 'tipopagina': 'sidebar-mini',
                           'form': formeditgroup})
    else:
        return redirect('/login')


def grupocontactoeliminar(request, idgrupocontacto):
    if request.user.is_authenticated:
        grupoccontacto = GrupoContactos.objects.get(id=idgrupocontacto)
        grupoccontacto.delete()
        messages.success(request, 'Grupo de Contactos eliminado correctamente')
        return redirect('/grupocontactos')
    else:
        return redirect('/login')


def telefononuevo(request, personaid):
    if request.user.is_authenticated:
        formtelefono = TelefonoPersonaCreateForm()
        if request.method == 'POST':
            request.POST._mutable = True
            request.POST['codPersona'] = str(personaid)
            request.POST._mutable = False
            formtelefono = TelefonoPersonaCreateForm(request.POST)
            if formtelefono.is_valid():
                newtelefono = formtelefono.save(commit=False)
                newtelefono.save()
                messages.success(request, 'Telefono Guardado Correctamente')
                return redirect('contactos')
            else:
                messages.error(request, 'Error Al guardar el nuevo Telefono')
        return render(request, 'pages/telefonoadd.html',
                      {'titlepage': 'Nuevo Telefono Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formtelefono})
    else:
        return redirect('login')


def telefonoeditar(request, telefonoid):
    if request.user.is_authenticated:
        telefono = TelefonoPersona.objects.get(id=telefonoid)
        formedittelefono = TelefonoPersonaEditForm(instance=telefono)
        if request.method == 'POST':
            formedittelefono = TelefonoPersonaEditForm(request.POST, instance=telefono)
            if formedittelefono.is_valid():
                telefonoedit = formedittelefono.save(commit=False)
                telefonoedit.save()
                messages.success(request, 'Datos del Telefono Editados Correctamente')
                return redirect('contactos')
            else:
                messages.error(request, 'No se pudo guardar los cambio de los datos del Telefono')
        return render(request, 'pages/telefonoedit.html',
                      {'titlepage': 'Editar Telefono Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formedittelefono})
    else:
        return redirect('login')


def telefonoeliminar(request, telefonoid):
    if request.user.is_authenticated:
        telefonodelete = TelefonoPersona.objects.get(id=telefonoid)
        telefonodelete.delete()
        messages.success(request, 'Telefono eliminado Correctamente')
        return redirect('contactos')
    else:
        return redirect('login')


def correonuevo(request, personaid):
    if request.user.is_authenticated:
        formcorreonew = CorreoPersonaCreateForm()
        if request.method == 'POST':
            request.POST._mutable = True
            request.POST['codPersona'] = str(personaid)
            request.POST._mutable = False
            formcorreonew = CorreoPersonaCreateForm(request.POST)
            if formcorreonew.is_valid():
                correonuevo = formcorreonew.save(commit=False)
                correonuevo.save()
                messages.success(request, 'Correo del Contacto Guardado')
                return redirect('contactos')
            else:
                messages.error(request, 'No se pudo guardar el correo especificado')
        return render(request, 'pages/correoadd.html',
                      {'titlepage': 'Nuevo Correo del Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formcorreonew})
    else:
        return redirect('login')


def correoeditar(request, correoid):
    if request.user.is_authenticated:
        correo = CorreoPersona.objects.get(id=correoid)
        formcorreoedit = CorreoPersonaEditForm(instance=correo)
        if request.method == 'POST':
            formcorreoedit = CorreoPersonaEditForm(request.POST, instance=correo)
            if formcorreoedit.is_valid():
                correoeditado = formcorreoedit.save(commit=False)
                correoeditado.save()
                messages.success(request, 'Correo Editado con exito')
                return redirect('contactos')
            else:
                messages.error(request, 'El correo no se pudo editar correctamente')
        return render(request, 'pages/correoedit.html',
                      {'titlepage': 'Editar Correo del Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formcorreoedit})
    else:
        return redirect('login')


def correoeliminar(request, correoid):
    if request.user.is_authenticated:
        correodelete = CorreoPersona.objects.get(id=correoid)
        correodelete.delete()
        messages.success(request, 'Correo eliminado Correctamente')
        return redirect('contactos')
    else:
        return redirect('login')


def direccionnueva(request, personaid):
    if request.user.is_authenticated:
        formdirecnew = DireccionPerosnaCreateForm()
        if request.method == 'POST':
            request.POST._mutable = True
            request.POST['codPersona'] = str(personaid)
            request.POST._mutable = False
            formdirecnew = DireccionPerosnaCreateForm(request.POST)
            if formdirecnew.is_valid():
                direccionnueva = formdirecnew.save(commit=False)
                direccionnueva.save()
                messages.success(request, 'Nueva Dirrecion de Contacto Agregada con exito')
                return redirect('contactos')
            else:
                messages.error(request, 'No se pudo Agregar Correctamente la direccion nueva')

        return render(request, 'pages/direccionadd.html',
                      {'titlepage': 'Añadir Direcion del Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formdirecnew})

    else:
        return redirect('login')


def direccioneditar(request, direccionid):
    if request.user.is_authenticated:
        direccioncontacto = DireccionPersona.objects.get(id=direccionid)
        formdirecedit = DireccionPersonaEditForm(instance=direccioncontacto)
        if request.method == 'POST':
            formdirecedit = DireccionPersonaEditForm(request.POST, instance=direccioncontacto)
            if formdirecedit.is_valid():
                direccioneditada = formdirecedit.save(commit=False)
                direccioneditada.save()
                messages.success(request, 'Dirrecion de Contacto Editada con exito')
                return redirect('contactos')
            else:
                messages.error(request, 'No se pudo Editar los datos Correctamente de la direccion')

        return render(request, 'pages/direccionedit.html',
                      {'titlepage': 'Editar Direccion del Contacto', 'tipopagina': 'sidebar-mini',
                       'form': formdirecedit})

    else:
        return redirect('login')


def direccioneliminar(request, direccionid):
    if request.user.is_authenticated:
        direccioncontacto = DireccionPersona.objects.get(id=direccionid)
        direccioncontacto.delete()
        messages.success(request, 'Direccion eliminado Correctamente')
        return redirect('contactos')

    else:
        return redirect('login')

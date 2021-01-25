from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Usuario, Persona, GrupoContactos, Contacto, ContactoGrupoContactos, TelefonoPersona, \
    DireccionPersona, CorreoPersona


class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']


class UsuarioUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'codPersona']


class UsuarioUserCreationFormInvitado(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'codPersona']
        exclude = ['password']


class UsuarioUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']


class UsuarioUpdateForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']


class PersonaCreateForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'fechaNacimiento']
        # fields = ['nombre', 'apellido', 'fechaNacimiento', 'foto']


class PersonaUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajo'].required = False
        self.fields['alias'].required = False
        self.fields['web'].required = False
        self.fields['identificacion'].required = False

    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'fechaNacimiento', 'trabajo', 'alias', 'web', 'identificacion', 'foto']
        # widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'})}


class PersonaCreateContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trabajo'].required = False
        self.fields['alias'].required = False
        self.fields['web'].required = False
        self.fields['identificacion'].required = False

    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'fechaNacimiento', 'trabajo', 'alias', 'web', 'identificacion', 'foto']
        # widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        #            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        #            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control'}),
        #            'trabajo': forms.TextInput(attrs={'class': 'form-control'}),
        #            'alias': forms.TextInput(attrs={'class': 'form-control'}),
        #            'web': forms.TextInput(attrs={'class': 'form-control'}),
        #            'identificacion': forms.TextInput(attrs={'class': 'form-control'})}
        # exclude = ['trabajo', 'alias', 'web', 'identificacion', 'foto']


class ContactoCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codPersona'].required = False

    class Meta:
        model = Contacto
        fields = ['codPersona']

        # widgets = {'codPersona':forms.TextInput(attrs={'class': 'form-control'})}


class ContactoGrupoContactoAddForm(ModelForm):
    # Para filtrar resultados en un foreing key
    def __init__(self, usuarioid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codContacto'].required = False
        self.fields['codGrupo'].queryset = GrupoContactos.objects.filter(codUsuario=usuarioid)

    class Meta:
        model = ContactoGrupoContactos
        fields = ['codContacto', 'codGrupo']
        labels = {'codGrupo': 'Seleccione el Grupo al que pertenecera el nuevo contacto'}
        # widgets = {'codContacto': forms.TextInput()}


class GrupoContactoCreateForm(ModelForm):
    class Meta:
        model = GrupoContactos
        fields = ['nombreGrupo', 'codUsuario']


class GrupoContactoEditForm(ModelForm):
    class Meta:
        model = GrupoContactos
        fields = ['nombreGrupo']


class ContactoGrupoContactoCreateForm(ModelForm):
    class Meta:
        model = ContactoGrupoContactos
        fields = ['codContacto', 'codGrupo']


class TelefonoPersonaCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codPersona'].required = False

    class Meta:
        model = TelefonoPersona
        fields = ['numeroTelefono', 'codPersona', 'detalleTelefono']


class TelefonoPersonaEditForm(ModelForm):
    class Meta:
        model = TelefonoPersona
        fields = ['numeroTelefono', 'detalleTelefono']


class CorreoPersonaCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codPersona'].required = False

    class Meta:
        model = CorreoPersona
        fields = ['Correo', 'codPersona']


class CorreoPersonaEditForm(ModelForm):
    class Meta:
        model = CorreoPersona
        fields = ['Correo']

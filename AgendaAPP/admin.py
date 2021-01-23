from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *


class UsuarioAdmin(UserAdmin):
    add_form = UsuarioUserCreationForm
    form = UsuarioUserChangeForm
    model = Usuario
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password','codPersona')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','codPersona', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


# Register your models here.

admin.site.register(Persona)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Contacto)
admin.site.register(GrupoContactos)
admin.site.register(ContactoGrupoContactos)
admin.site.register(DireccionPersona)
admin.site.register(CorreoPersona)
admin.site.register(DetalleTelefono)
admin.site.register(TelefonoPersona)

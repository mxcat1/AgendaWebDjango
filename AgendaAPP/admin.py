from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Contacto)
admin.site.register(GrupoContactos)
admin.site.register(ContactoGrupoContactos)
admin.site.register(DireccionPersona)
admin.site.register(CorreoPersona)
admin.site.register(DetalleTelefono)
admin.site.register(TelefonoPersona)
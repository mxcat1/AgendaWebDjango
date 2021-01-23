from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def upload_location(instance, filename):
    path = f'Personas/{str(instance.id)}/ {filename}'
    return path


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Persona(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    fechaNacimiento = models.DateField()
    trabajo = models.CharField(max_length=100, null=True)
    alias = models.CharField(max_length=100, null=True)
    web = models.CharField(max_length=250, null=True)
    identificacion = models.CharField(max_length=15, null=True)
    foto = models.ImageField(null=True, upload_to=upload_location, default='Personas/perfil.jpg')

    class Meta:
        verbose_name = 'Persona'

    def __str__(self):
        return f'{self.id}) {self.nombre}'


class Usuario(AbstractUser):
    # nombreUsuario = models.CharField(max_length=150, unique=True)
    # emailSuperuser = models.EmailField()
    # is_active = models.BooleanField(default=True)
    # contrasenia = models.CharField(max_length=150)
    codPersona = models.OneToOneField(Persona, null=True, on_delete=models.SET_NULL, related_name='Usuario')

    # USERNAME_FIELD = 'nombreUsuario'
    # EMAIL_FIELD = 'emailSuperuser'
    # REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['codPersona']
    # class Meta:
    #     verbose_name = 'Usuario'

    # def __str__(self):
    #     return f'{self.id}-{self.codPersona}) {self.nombreUsuario} Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'


class Contacto(TimeStampMixin):
    codPersona = models.OneToOneField(Persona, null=True, on_delete=models.SET_NULL, related_name='Contacto')

    class Meta:
        verbose_name = 'Contacto'

    def __str__(self):
        return f'{self.id}-{self.codPersona}) Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'


class GrupoContactos(TimeStampMixin):
    codUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombreGrupo = models.CharField(max_length=150)
    contactos = models.ManyToManyField(Contacto, through='ContactoGrupoContactos',
                                       through_fields=('codGrupo', 'codContacto'))

    class Meta:
        verbose_name = 'GrupoContactos'
        verbose_name_plural = 'GrupoContactos'

    def __str__(self):
        return f'{self.id}-{self.nombreGrupo}'


class ContactoGrupoContactos(TimeStampMixin):
    codGrupo = models.ForeignKey(GrupoContactos, on_delete=models.CASCADE, default='Por Defecto')
    # codContacto = models.ForeignKey(Contacto, on_delete=models.CASCADE)
    codContacto = models.ForeignKey(Contacto, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'ContactoGrupoContactos'
        verbose_name_plural = 'ContactoGrupoContactos'

    def __str__(self):
        return f'{self.id}-{self.codGrupo}-{self.codContacto}) Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'


class DireccionPersona(TimeStampMixin):
    opcionesTipoDireccion = (('Casa', 'Casa'), ('Trabajo', 'Trabajo'), ('Otros', 'Otros'))

    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipoDireccion = models.CharField(max_length=50, choices=opcionesTipoDireccion, default='Casa')
    direccion = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'DireccionPersona'

    def __str__(self):
        return f'{self.id}) {self.tipoDireccion} {self.direccion} Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'


class CorreoPersona(TimeStampMixin):
    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    Correo = models.EmailField()

    class Meta:
        verbose_name = 'CorreoPersona'

    def __str__(self):
        return f'{self.id}-{self.codPersona}) {self.correo} Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'


class DetalleTelefono(TimeStampMixin):
    opcionesTipo = (('Hogar', 'Hogar'), ('Celular', 'Celular'), ('Otros', 'Otros'))

    tipo = models.CharField(max_length=100, choices=opcionesTipo, default='Celular')
    operador = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'DetalleTelefono'

    def __str__(self):
        return f'{self.tipo} {self.operador}'


class TelefonoPersona(TimeStampMixin):
    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    numeroTelefono = models.CharField(max_length=15, default='000000000')
    detalleTelefono = models.ForeignKey(DetalleTelefono, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TelefonoPersona'

    def __str__(self):
        return f'{self.id}-{self.codPersona}) {self.numeroTelefono} Fecha Creacion {self.created_at} Fecha Actualizacion {self.updated_at}'

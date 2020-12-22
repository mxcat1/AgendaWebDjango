from django.db import models


# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    fechaNacimiento = models.DateField()
    trabajo = models.CharField(max_length=100, null=True)
    alias = models.CharField(max_length=100, null=True)
    web = models.CharField(max_length=250, null=True)
    identificacion = models.CharField(max_length=15, null=True)
    foto = models.TextField(max_length=500, null=True)


class Usuario(models.Model):
    nombreUsuario = models.CharField(max_length=150)
    contrasenia = models.CharField(max_length=150)
    codPersona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='Usuario')


class Contacto(models.Model):
    codPersona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='Contacto')


class GrupoContactos(models.Model):
    codUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombreGrupo = models.CharField(max_length=150)
    contactos = models.ManyToManyField(Contacto, through='ContactoGrupoContactos',
                                       through_fields=('codGrupo', 'codContacto'))


class ContactoGrupoContactos(models.Model):
    codGrupo = models.ForeignKey(GrupoContactos, on_delete=models.CASCADE)
    codContacto = models.ForeignKey(Contacto, on_delete=models.CASCADE)


class DireccionPersona(models.Model):
    opcionesTipoDireccion = (('Casa', 'Casa'), ('Trabajo', 'Trabajo'), ('Otros', 'Otros'))

    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tipoDireccion = models.CharField(max_length=50, choices=opcionesTipoDireccion, default='Casa')
    direccion = models.CharField(max_length=500)


class CorreoPersona(models.Model):
    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    Correo = models.EmailField()


class DetalleTelefono(models.Model):
    opcionesTipo = (('Hogar', 'Hogar'), ('Celular', 'Celular'), ('Otros', 'Otros'))

    tipo = models.CharField(max_length=100, choices=opcionesTipo, default='Celular')
    operador = models.CharField(max_length=100)


class TelefonoPersona(models.Model):
    codPersona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    numeroTelefono = models.CharField(max_length=15, default='000000000')
    detalleTelefono = models.ForeignKey(DetalleTelefono, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    categoria = models.CharField(max_length=50, blank=True, null=True)
    
class Empleado(models.Model):
    legajo = models.CharField(max_length=20, unique=True)  # Número de legajo
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    # categoria = models.OneToOneField(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    # edad = models.PositiveIntegerField(blank=True, null=True)  # opcional, se puede calcular
    sector = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.CharField(max_length=100, blank=True, null=True)

    # Relación con usuario del sistema
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    cuil = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    nombre_contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono_emergencia = models.CharField(max_length=20, blank=True, null=True)
    mail = models.EmailField(blank=True, null=True)
    domicilio = models.CharField(max_length=200, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)

    ingreso_empresa = models.DateField(blank=True, null=True)
    ingreso_pct = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (Legajo {self.legajo})"


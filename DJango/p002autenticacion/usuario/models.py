from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'


# =====================================================
# NUEVO MODELO: Personal (para el ABM de empleados)
# =====================================================
class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cargo = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

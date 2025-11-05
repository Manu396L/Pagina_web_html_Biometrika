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

    # 👇 Relación con Ubicación (sede)
    ubicacion = models.ForeignKey(
        'Ubicacion',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='empleados'
    )

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


# =====================================================
# NUEVO MODELO: Ubicación (para gestión de sedes y áreas)
# =====================================================
class Ubicacion(models.Model):
    TIPO_CHOICES = [
        ('sede', 'Sede (Edificio Principal)'),
        ('oficina', 'Oficina (Piso/Ala)'),
        ('area', 'Área Específica (Sala/Cuarto)'),
    ]

    DISPOSITIVO_CHOICES = [
        ('huella', 'Lector de Huella Dactilar'),
        ('Tarjeta', 'Tarjeta de Acceso'),
        ('PIN', 'PIN'),
    ]

    SEGURIDAD_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ]

    tipo_ubicacion = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nombre_sede = models.CharField(max_length=100)
    codigo_unico = models.CharField(max_length=50, unique=True)
    direccion = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    dispositivo_biometrico = models.CharField(
        max_length=20, choices=DISPOSITIVO_CHOICES, blank=True, null=True
    )
    nivel_seguridad = models.CharField(
        max_length=20, choices=SEGURIDAD_CHOICES, blank=True, null=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre_sede']

    def __str__(self):
        return f"{self.nombre_sede} ({self.codigo_unico})"

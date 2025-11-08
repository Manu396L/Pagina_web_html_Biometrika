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

#=============================================0
#               DISPOSITIVOS
#==============================================


class Dispositivo(models.Model):
    TIPO_SEDE_CHOICES = [
        ('SEDE_PRINCIPAL', 'Sede Principal'),
        ('ALMACEN', 'Almacén'),
        ('OFICINA', 'Oficina'),
    ]

    TIPO_DISPOSITIVO_CHOICES = [
        ('Lector de Huella', 'Lector de Huella'),
        ('Lector de Iris', 'Lector de Iris'),
        ('Reconocimiento Facial', 'Reconocimiento Facial'),
        ('Tarjeta RFID', 'Tarjeta RFID'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('PAUSADO', 'Pausado'),
        ('INACTIVO', 'Inactivo'),
    ]

    ZONA_CHOICES = [
        ('America/Argentina/Buenos_Aires', 'Buenos Aires (GMT-3)'),
        ('America/Cordoba', 'Córdoba (GMT-3)'),
        ('America/Mendoza', 'Mendoza (GMT-3)'),
    ]

    # Información Básica
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Dispositivo")
    numero_serie = models.CharField(max_length=50, unique=True, verbose_name="Número de Serie")
    tipo_sede = models.CharField(max_length=20, choices=TIPO_SEDE_CHOICES, verbose_name="Tipo de Sede")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispositivos')
    direccion_fisica = models.TextField(blank=True, null=True, verbose_name="Dirección Física")

    # Configuración de Red
    direccion_ip = models.GenericIPAddressField(verbose_name="Dirección IP")
    zona_horaria = models.CharField(max_length=50, choices=ZONA_CHOICES, verbose_name="Zona Horaria")
    intervalo_solicitud = models.IntegerField(default=5, verbose_name="Intervalo de Solicitud (minutos)")

    # Estado y Configuración
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado del Dispositivo")
    tipo_dispositivo = models.CharField(max_length=30, choices=TIPO_DISPOSITIVO_CHOICES, verbose_name="Tipo de Dispositivo")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_conexion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

    def __str__(self):
        return f"{self.nombre} - {self.numero_serie}"
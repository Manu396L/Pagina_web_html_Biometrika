from django.db import models

class Task(models.Model):
    title = models.CharField(max_length= 100)
    description = models.TextField(blank= True)
    is_completed = models.BooleanField(default= False)
    created = models.DateTimeField(auto_now= True)

    class Meta:
        ordering= ['created']
    
    def __str__(self):
        return self.title
    
class Edificio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    descripcion = models.TextField()
    #empleados_autorizados = models.ManyToManyField('Empleado', related_name='edificios_autorizados', blank=True)

    def __str__(self):
        return self.nombre
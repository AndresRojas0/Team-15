from django.db import models
from materia.models import Materia

class Planificacion(models.Model):
    materia = models.OneToOneField(Materia, on_delete=models.CASCADE, related_name='planificacion')
    fecha_inicio = models.CharField(max_length=10, null=True, blank=True)
    fecha_fin = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.materia.nombre} - {self.fecha_inicio} a {self.fecha_fin}"
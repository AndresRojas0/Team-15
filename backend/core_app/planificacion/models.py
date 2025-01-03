from django.db import models
from materia.models import Materia

class Planificacion(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='planificaciones')
    nombre_unidad = models.CharField(max_length=100)
    nombre_tema = models.CharField(max_length=255)
    fecha_inicio = models.CharField(max_length=10)
    fecha_fin = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.nombre_unidad = self.nombre_unidad.lower()
        self.nombre_tema = self.nombre_tema.lower()
        self.fecha_inicio = self.fecha_inicio.lower()
        self.fecha_fin = self.fecha_fin.lower()
        super(Planificacion, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_unidad}, {self.nombre_tema}, {self.fecha_inicio}, {self.fecha_fin}"
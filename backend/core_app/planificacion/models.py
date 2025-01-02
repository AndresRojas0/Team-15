from django.db import models
from curso.models import Curso
from materia.mmodels import Materia

class Planificacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='planificaciones')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='planificaciones')
    nombre_unidad = models.CharField(max_length=100)
    nombre_tema = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.nombre_unidad = self.nombre_unidad.lower()
        self.nombre_tema = self.nombre_tema.lower()
        super(Planificacion, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_unidad}, {self.nombre_tema}"
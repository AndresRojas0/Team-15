from django.db import models
from curso.models import Curso

class Periodo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='periodos')
    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()

    def __str__(self):
        return f"{self.curso.nombre} - {self.fecha_inicio} a {self.fecha_cierre}"
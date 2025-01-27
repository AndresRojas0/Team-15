from django.db import models
from planificacion_diaria.models import PlanificacionDiaria

class Recurso(models.Model):
    planificacion_diaria = models.ForeignKey(PlanificacionDiaria, on_delete=models.CASCADE, related_name='recursos')
    fecha = models.DateField()
    url = models.URLField(max_length=500)

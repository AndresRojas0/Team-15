from django.db import models
from planificacion.models import Planificacion

class PlanificacionDiaria(models.Model):
    planificacion_id = models.ForeignKey(Planificacion, on_delete=models.CASCADE, related_name='planificacion_diaria')
    fecha = models.DateField()
    tipo_clase = models.CharField(max_length=50)
    detalle = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['planificacion_id', 'fecha'], name='unique_planificacion_fecha')
        ]
from django.db import models
from subtema.models import Subtema
from planificacion.models import Planificacion

class PlanificacionMensual(models.Model):
    planificacion_id = models.ForeignKey(Planificacion, on_delete=models.CASCADE, related_name='planificacion_mensual')
    subtema_id = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    fecha = models.DateField()
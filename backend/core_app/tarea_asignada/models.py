from django.db import models
from subtema.models import Subtema
from periodo.models import Periodo
from materia.models import Materia

# Create your models here.
class TareaAsignada(models.Model):
    materia_id = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='tareas_asignadas', null=True)
    subtema_id = models.ForeignKey(Subtema, on_delete=models.CASCADE)
    periodo_id = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    fecha = models.DateField(null=True)

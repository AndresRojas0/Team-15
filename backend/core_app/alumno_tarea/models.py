from django.db import models
from alumno.models import Alumno
from tarea_asignada.models import TareaAsignada

# Create your models here.
class AlumnoTarea(models.Model):
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, related_name='alumno_tareas')
    tarea_asignada_id = models.ForeignKey(TareaAsignada, on_delete=models.CASCADE, null=True, related_name='alumno_tareas')
    fecha = models.DateField()
    tipo_calificacion = models.CharField(max_length=50)
    calificacion_binaria = models.BooleanField(null=True)
    calificacion_numerica = models.FloatField(null=True)
    calificacion_conceptual = models.CharField(max_length=60, null=True)
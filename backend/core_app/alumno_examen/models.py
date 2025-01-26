from django.db import models
from alumno.models import Alumno
from examen_asignado.models import ExamenAsignado

# Create your models here.
class AlumnoExamen(models.Model):
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, related_name='alumno_examenes')
    examen_asignado_id = models.ForeignKey(ExamenAsignado, on_delete=models.CASCADE, null=True, related_name='alumno_examenes')
    fecha = models.DateField()
    tipo_calificacion = models.CharField(max_length=50, null=True)
    calificacion_binaria = models.BooleanField(null=True)
    calificacion_numerica = models.FloatField(null=True)
    calificacion_conceptual = models.CharField(max_length=60, null=True)
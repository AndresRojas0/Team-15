from django.db import models
from alumno.models import Alumno
from examen_asignado.models import ExamenAsignado

# Create your models here.
class AlumnoExamen(models.Model):
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, related_name='alumno_examenes')
    examen_asignado_id = models.ForeignKey(ExamenAsignado, on_delete=models.CASCADE, null=True, related_name='alumno_examenes')
    fecha = models.DateField()
    calificacion = models.FloatField(null=True)
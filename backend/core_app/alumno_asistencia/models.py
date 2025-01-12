from django.db import models
from alumno.models import Alumno
from curso.models import Curso

# Create your models here.
class AlumnoAsistencia(models.Model):
    curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='alumno_asistencia')
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='alumno_asistencia')
    nombre_valoracion = models.CharField(max_length=50)
    fecha = models.DateField()
    falta_justificada = models.BooleanField(default=False)

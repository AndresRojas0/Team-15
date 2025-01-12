from django.db import models
from alumno.models import Alumno
from curso.models import Curso

# Create your models here.
class AlumnoActitudinal(models.Model):
    alumno_id = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='alumno_actitudinal')
    curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='alumno_actitudinal')
    nombre_valoracion = models.CharField(max_length=50)
    fecha = models.DateField()
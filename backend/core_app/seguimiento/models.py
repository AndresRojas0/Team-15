from django.db import models
from curso.models import Curso
from alumno.models import Alumno

class Seguimiento(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='seguimientos')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='seguimientos')
    calificaciones = models.IntegerField(null = True)
    asistencia = models.CharField(max_length=255)
    anotaciones = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.calificaciones = self.calificaciones
        self.asistencia = self.asistencia.lower()
        self.anotaciones = self.anotaciones.lower()
        super(Seguimiento, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.calificaciones}, {self.asistencia}, {self.anotaciones}"
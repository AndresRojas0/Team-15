from django.db import models
from alumno.models import Alumno
from planificacion.models import Planificacion

class Seguimiento(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='seguimientos')
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE, related_name='seguimientos', null=True, blank=True)
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
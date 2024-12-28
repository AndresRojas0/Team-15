from django.db import models
from curso.models import Curso

class Planificacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='planificaciones')
    tipo = models.CharField(max_length=50)
    contenido = models.CharField(max_length=255)
    metodologia= models.CharField(max_length=255)
    anotaciones = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.tipo = self.tipo.lower()
        self.contenido = self.contenido.lower()
        self.metodologia = self.metodologia.lower()
        self.anotaciones = self.anotaciones.lower()
        super(Planificacion, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo}, {self.contenido}, {self.metodologia}, {self.anotaciones}"
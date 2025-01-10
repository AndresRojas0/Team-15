from django.db import models
from curso.models import Curso

class Recurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='recursos')
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=600, blank=True, null=True)
    url = models.CharField(max_length=600)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()
        self.descripcion = self.descripcion.lower()
        self.url = self.url.lower()
        super(Recurso, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.descripcion}, {self.url}"
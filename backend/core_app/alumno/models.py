from django.db import models
from curso.models import Curso

class Alumno(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='alumnos')
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()  # Convierte el nombre a minúsculas
        self.apellido = self.apellido.lower()  # Convierte el apellido a minúsculas
        super(Alumno, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
from django.db import models
from institucion.models import Institucion

class Curso(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='cursos')
    nombre = models.CharField(max_length=255)
    duracion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucion', 'nombre'], name='unique_curso_per_institucion')
        ]

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()  # Convierte el nombre a minúsculas
        super(Curso, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
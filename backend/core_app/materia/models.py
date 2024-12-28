from django.db import models
from curso.models import Curso

class Materia(models.Model):
    curso = models.ForeignKey(Curso, related_name='materias', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['curso', 'nombre'], name='unique_materia_per_curso')
        ]

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()  # Convierte el nombre a minúsculas
        super(Materia, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
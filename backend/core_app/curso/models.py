from django.db import models
from institucion.models import Institucion

class Curso(models.Model):
    CUATRIMESTRAL = 'CU'
    TRIMESTRAL = 'TR'
    BIMESTRAL = 'BI'
    ANUAL = 'AN'

    DURACION_CHOICES = [
        (CUATRIMESTRAL, 'Cuatrimestral'),
        (TRIMESTRAL, 'Trimestral'),
        (BIMESTRAL, 'Bimestral'),
        (ANUAL, 'Anual'),
    ]

    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='cursos')
    nombre = models.CharField(max_length=255)
    duracion = models.CharField(max_length=2, choices=DURACION_CHOICES, default=ANUAL)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['institucion', 'nombre'], name='unique_curso_per_institucion')
        ]

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()  # Convierte el nombre a minúsculas
        super(Curso, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
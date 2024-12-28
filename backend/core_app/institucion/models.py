from django.db import models
from django.contrib.auth import get_user_model

class Institucion(models.Model):
    docente = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['docente', 'nombre'], name='unique_institucion_per_docente')
        ]

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()  # Convierte el nombre a minúsculas
        super(Institucion, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
from django.db import models

class Subtema(models.Model):
    id_tema = models.ForeignKey('tema.Tema', on_delete=models.CASCADE, related_name='subtemas')
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.CharField(max_length=10, null=True, blank=True, default=None)
    fecha_fin = models.CharField(max_length=10, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre
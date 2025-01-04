from django.db import models

class Tema(models.Model):
    id_planificacion = models.ForeignKey('planificacion.Planificacion', on_delete=models.CASCADE, related_name='temas')
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.CharField(max_length=10, null=True, blank=True, default=None)
    fecha_fin = models.CharField(max_length=10, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombre
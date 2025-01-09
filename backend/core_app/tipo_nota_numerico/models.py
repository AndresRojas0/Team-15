from django.db import models

# Create your models here.
class TipoNotaNumerico(models.Model):
    nota_minima = models.IntegerField()
    nota_maxima = models.IntegerField()
    rango_minimo = models.IntegerField()
    es_un_examen = models.BooleanField(default=False)
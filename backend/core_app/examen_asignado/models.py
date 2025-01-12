from django.db import models
from tema.models import Tema
from periodo.models import Periodo
from materia.models import Materia

# Create your models here.
class ExamenAsignado(models.Model):
    materia_id = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='examenes_asignados', null=True)
    tema_id = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='examenes_asignados', null=True)
    periodo_id = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='examenes_asignados', null=True)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100) # regular o recuperatorio
    fecha = models.DateField()
    es_recuperatorio = models.BooleanField(default=False)
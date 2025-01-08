from django.db import models
from curso.models import Curso
from tipo_nota_binario.models import TipoNotaBinario
from tipo_nota_numerico.models import TipoNotaNumerico

class SistemaNotas(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='sistema_notas')
    porcentaje_examenes = models.IntegerField()
    porcentaje_tareas = models.IntegerField()
    porcentaje_actitudinal = models.IntegerField()
    tipo_nota = models.CharField(max_length=50)  # numerico, conceptual, actitudinal
    tipo_nota_numerico = models.ForeignKey(TipoNotaNumerico, on_delete=models.CASCADE, related_name='sistema_notas_numerico', null=True, blank=True)
    tipo_nota_binario = models.ForeignKey(TipoNotaBinario, on_delete=models.CASCADE, related_name='sistema_notas_binario', null=True, blank=True)
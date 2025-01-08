from django.db import models
from sistema_notas.models import SistemaNotas

class TipoNotaConceptual(models.Model):
    nombre = models.CharField(max_length=50)
    valoracion = models.IntegerField()
    sistema_notas = models.ForeignKey(SistemaNotas, on_delete=models.CASCADE, related_name='tipo_nota_conceptual', default=1)

    def __str__(self):
        return self.nombre
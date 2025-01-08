from django.db import models
from subtema.models import Subtema

class SubtemaAnual(models.Model):
    subtema_id = models.ForeignKey(Subtema, on_delete=models.CASCADE, related_name='subtemas_anuales', db_column='subtema_id')
    mes = models.IntegerField()
    año = models.IntegerField()

    def __str__(self):
        return f"{self.subtema_id.nombre} - {self.mes}/{self.año}"
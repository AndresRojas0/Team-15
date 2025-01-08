from django.db import models

# Create your models here.
class TipoNotaBinario(models.Model):
    aprobado = models.BooleanField()

from django.db import models
from recursos.models import Recurso

class RecursoURL(models.Model):
    recurso_id = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name='recursos')
    url = models.FileField(upload_to ='uploads/% Y/% m/% d/', null=True, blanck=True)
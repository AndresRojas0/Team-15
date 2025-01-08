from rest_framework import serializers
from .models import Periodo

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ['id', 'curso_id', 'fecha_inicio', 'fecha_cierre']
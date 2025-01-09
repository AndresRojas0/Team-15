from rest_framework import serializers
from .models import PlanificacionMensual

class PlanificacionMensualSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionMensual
        fields = '__all__'
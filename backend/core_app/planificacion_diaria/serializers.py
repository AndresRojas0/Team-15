from rest_framework import serializers
from .models import PlanificacionDiaria

class PlanificacionDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDiaria
        fields = '__all__'


class PlanificacionDiariaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDiaria
        fields = '__all__'

class UpdatePlanificacionDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDiaria
        fields = '__all__'
        read_only_fields = ['planificacion_id']
from rest_framework import serializers
from recursos.serializers import RecursoSerializer
from .models import PlanificacionDiaria

class PlanificacionDiariaSerializer(serializers.ModelSerializer):
    recursos = RecursoSerializer(many=True, read_only=True)

    class Meta:
        model = PlanificacionDiaria
        fields = ['id', 'planificacion_id', 'fecha', 'tipo_clase', 'detalle', 'recursos']


class PlanificacionDiariaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDiaria
        fields = '__all__'

class UpdatePlanificacionDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionDiaria
        fields = '__all__'
        read_only_fields = ['planificacion_id']
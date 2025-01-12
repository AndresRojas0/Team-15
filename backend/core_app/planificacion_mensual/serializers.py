from rest_framework import serializers
from .models import PlanificacionMensual
from subtema.models import Subtema

class PlanificacionMensualSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanificacionMensual
        fields = '__all__'


class UpdatePlanificacionMensualSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)
    subtema_id = serializers.PrimaryKeyRelatedField(queryset=Subtema.objects.all(), required=False)

    class Meta:
        model = PlanificacionMensual
        fields = '__all__'
        read_only_fields = ['planificacion_id']
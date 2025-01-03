from rest_framework import serializers
from .models import Planificacion
from materia.models import Materia

class PlanificacionSerializer(serializers.ModelSerializer):
    materia_id = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all(), source='materia')

    class Meta:
        model = Planificacion
        fields = ['id', 'materia_id', 'nombre_unidad', 'nombre_tema', 'fecha_inicio', 'fecha_fin']

class RegisterPlanificacionSerializer(serializers.Serializer):
    planificaciones = PlanificacionSerializer(many=True)

    def create(self, validated_data):
        planificaciones_data = validated_data.pop('planificaciones')
        planificaciones = []
        for planificacion_data in planificaciones_data:
            planificacion = Planificacion.objects.create(**planificacion_data)
            planificaciones.append(planificacion)
        return {'planificaciones': planificaciones}
from rest_framework import serializers
from .models import Planificacion
from curso.models import Curso
from materia.models import Materia

class PlanificacionSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')
    materia_id = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all(), source='materia')

    class Meta:
        model = Planificacion
        fields = ['id', 'curso_id', 'materia_id', 'nombre_unidad', 'nombre_tema']

class RegisterPlanificacionSerializer(serializers.Serializer):
    planificaciones = PlanificacionSerializer(many=True)

    def create(self, validated_data):
        planificaciones_data = validated_data.pop('planificaciones')
        planificaciones = []
        for planificacion_data in planificaciones_data:
            planificacion = Planificacion.objects.create(**planificacion_data)
            planificaciones.append(planificacion)
        return {'planificaciones': planificaciones}
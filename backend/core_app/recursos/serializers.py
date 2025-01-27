from rest_framework import serializers
from planificacion_diaria.models import PlanificacionDiaria
from .models import Recurso

class RecursoSerializer(serializers.ModelSerializer):
    planificacion_diaria_id = serializers.IntegerField(source='planificacion_diaria.id', read_only=True)

    class Meta:
        model = Recurso
        fields = ['id','planificacion_diaria_id', 'fecha', 'url']


class RegisterRecursoSerializer(serializers.ModelSerializer):
    planificacion_diaria = serializers.PrimaryKeyRelatedField(queryset=PlanificacionDiaria.objects.all(), write_only=True)
    planificacion_diaria_id = serializers.IntegerField(source='planificacion_diaria.id', read_only=True)

    class Meta:
        model = Recurso
        fields = ['planificacion_diaria', 'planificacion_diaria_id', 'fecha', 'url']

    def create(self, validated_data):
        return Recurso.objects.create(**validated_data)

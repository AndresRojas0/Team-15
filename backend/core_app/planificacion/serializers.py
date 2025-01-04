from rest_framework import serializers
from .models import Planificacion
from materia.models import Materia
from tema.serializers import RegisterTemaSerializer, TemaSerializer
from tema.models import Tema
from subtema.models import Subtema

class PlanificacionSerializer(serializers.ModelSerializer):
    temas = TemaSerializer(many=True, read_only=True)

    class Meta:
        model = Planificacion
        fields = ['id', 'materia', 'fecha_inicio', 'fecha_fin', 'temas']

1

class RegisterPlanificacionSerializer(serializers.ModelSerializer):
    materia_id = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all(), source='materia')
    temas = RegisterTemaSerializer(many=True)

    class Meta:
        model = Planificacion
        fields = ['id', 'materia_id', 'fecha_inicio', 'fecha_fin', 'temas']

    def create(self, validated_data):
        temas_data = validated_data.pop('temas')
        planificacion = Planificacion.objects.create(**validated_data)
        for tema_data in temas_data:
            subtemas = tema_data.pop('subtemas')
            tema = Tema.objects.create(id_planificacion=planificacion, nombre=tema_data['nombre'])
            for subtema_nombre in subtemas:
                Subtema.objects.create(id_tema=tema, nombre=subtema_nombre)
        return planificacion
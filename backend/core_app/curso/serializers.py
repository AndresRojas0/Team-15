# filepath: /c:/Users/crist/Desktop/Foo Talent Group/Team-15/backend/core_app/curso/serializers.py
from rest_framework import serializers

from periodo.models import Periodo
from periodo.serializers import PeriodoSerializer
from materia.serializers import MateriaSerializer
from .models import Curso

class CursoSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)
    periodos = PeriodoSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'institucion_id', 'nombre', 'duracion', 'periodos', 'materias']


class UpdateCursoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    nombre = serializers.CharField(required=True)

    class Meta:
        model = Curso
        fields = ['id', 'nombre']

class RegisterCursoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    institucion_id = serializers.IntegerField(required=True)
    periodos = PeriodoSerializer(many=True, write_only=True)

    class Meta:
        model = Curso
        fields = ['nombre', 'institucion_id', 'duracion', 'periodos']

    def create(self, validated_data):
        periodos_data = validated_data.pop('periodos')
        curso = Curso.objects.create(**validated_data)
        for periodo_data in periodos_data:
            Periodo.objects.create(curso=curso, **periodo_data)
        return curso

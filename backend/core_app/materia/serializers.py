# filepath: /c:/Users/crist/Desktop/Foo Talent Group/Team-15/backend/core_app/materia/serializers.py
from rest_framework import serializers
from planificacion.serializers import PlanificacionSerializer
from curso.models import Curso
from .models import Materia

class MateriaSerializer(serializers.ModelSerializer):
    planificacion = PlanificacionSerializer(read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'curso_id', 'nombre', 'planificacion']

class RegisterMateriaSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Materia
        fields = ['curso_id', 'nombre']

    def validate(self, data):
        curso_id = data.get('curso')
        nombre = data.get('nombre')
        if not curso_id:
            raise serializers.ValidationError("Course ID is required")
        if not nombre:
            raise serializers.ValidationError("Name is required")
        return data
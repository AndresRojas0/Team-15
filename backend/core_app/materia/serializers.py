# filepath: /c:/Users/crist/Desktop/Foo Talent Group/Team-15/backend/core_app/materia/serializers.py
from rest_framework import serializers
from examen_asignado.serializers import ExamenAsignadoSerializer
from planificacion.serializers import PlanificacionSerializer
from curso.models import Curso
from .models import Materia
from tarea_asignada.serializers import TareaAsignadaSerializer

class MateriaSerializer(serializers.ModelSerializer):
    planificacion = PlanificacionSerializer(read_only=True)
    tareas_asignadas = TareaAsignadaSerializer(many=True, read_only=True)
    examenes_asignados = ExamenAsignadoSerializer(many=True, read_only=True)

    class Meta:
        model = Materia
        fields = ['id', 'curso_id', 'nombre', 'planificacion', 'tareas_asignadas', 'examenes_asignados']

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
    

class UpdateSerializer(serializers.ModelSerializer):
    # curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso', required=False)

    class Meta:
        model = Materia
        fields = ['id', 'curso_id', 'nombre']
        read_only_fields = ['curso_id']


class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id']
        read_only_fields = ['id']
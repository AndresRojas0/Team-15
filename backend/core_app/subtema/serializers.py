from rest_framework import serializers
from tema.models import Tema
from .models import Subtema
from subtema_anual.serializers import SubtemaAnualSerializer

class SubtemaSerializer(serializers.ModelSerializer):
    subtemas_anuales = SubtemaAnualSerializer(many=True, read_only=True)

    class Meta:
        model = Subtema
        fields = ['id', 'id_tema', 'nombre', 'fecha_inicio', 'fecha_fin', 'subtemas_anuales']

class RegisterSubtemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtema
        fields = ['id', 'id_tema', 'nombre', 'fecha_inicio', 'fecha_fin']


class UpdateSubtemaSerializer(serializers.ModelSerializer):
    id_tema = serializers.PrimaryKeyRelatedField(queryset=Tema.objects.all(), required=False)
    nombre = serializers.CharField(required=False)
    # curso_id= serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), required=False)
    # alumno_id = serializers.PrimaryKeyRelatedField(queryset=Alumno.objects.all(), required=False)

    class Meta:
        model = Subtema
        fields = '__all__'
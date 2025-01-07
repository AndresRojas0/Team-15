from rest_framework import serializers
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
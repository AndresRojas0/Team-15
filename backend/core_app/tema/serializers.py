from rest_framework import serializers
from .models import Tema
from subtema.serializers import SubtemaSerializer

class RegisterTemaSerializer(serializers.ModelSerializer):
    tema = serializers.CharField(source='nombre')
    subtemas = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Tema
        fields = ['id', 'tema', 'unidad', 'subtemas']



class TemaSerializer(serializers.ModelSerializer):
    subtemas = SubtemaSerializer(many=True, read_only=True)

    class Meta:
        model = Tema
        fields = ['id', 'id_planificacion', 'nombre', 'unidad', 'fecha_inicio', 'fecha_fin', 'subtemas']


class RegisterOnlyTemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ['id', 'nombre', 'unidad', 'fecha_inicio', 'fecha_fin', 'id_planificacion']
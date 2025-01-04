from rest_framework import serializers
from .models import Subtema

class SubtemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtema
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin']
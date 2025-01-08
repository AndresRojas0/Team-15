from rest_framework import serializers

from curso.serializers import CursoSerializer
from .models import Institucion

class InstitucionSerializer(serializers.ModelSerializer):
    cursos = CursoSerializer(many=True, read_only=True)

    class Meta:
        model = Institucion
        fields = ['id', 'docente', 'nombre', 'cursos']
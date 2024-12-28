from rest_framework import serializers
from .models import Seguimiento
from curso.models import Curso
from alumno.models import Alumno

class SeguimientoSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')
    alumno_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='alumno')

    class Meta:
        model = Seguimiento
        fields = ['id', 'curso_id', 'alumno_id', 'calificaciones', 'asistencia', 'anotaciones']

class RegisterSeguimientoSerializer(serializers.Serializer):
    seguimientos = SeguimientoSerializer(many=True)

    def create(self, validated_data):
        seguimientos_data = validated_data.pop('seguimientos')
        seguimientos = []
        for seguimiento_data in seguimientos_data:
            seguimiento = Seguimiento.objects.create(**seguimiento_data)
            seguimientos.append(seguimiento)
        return {'seguimientos': seguimientos}
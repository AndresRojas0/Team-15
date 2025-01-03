from rest_framework import serializers
from .models import Seguimiento
from alumno.models import Alumno
from planificacion.models import Planificacion

class SeguimientoSerializer(serializers.ModelSerializer):
    alumno_id = serializers.PrimaryKeyRelatedField(queryset=Alumno.objects.all(), source='alumno')
    planificacion_id = serializers.PrimaryKeyRelatedField(queryset=Planificacion.objects.all(), source='planificacion')

    class Meta:
        model = Seguimiento
        fields = ['id', 'alumno_id', 'planificacion_id', 'calificaciones', 'asistencia', 'anotaciones']

class RegisterSeguimientoSerializer(serializers.Serializer):
    seguimientos = SeguimientoSerializer(many=True)

    def create(self, validated_data):
        seguimientos_data = validated_data.pop('seguimientos')
        seguimientos = []
        for seguimiento_data in seguimientos_data:
            seguimiento = Seguimiento.objects.create(**seguimiento_data)
            seguimientos.append(seguimiento)
        return {'seguimientos': seguimientos}
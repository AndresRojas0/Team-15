from rest_framework import serializers
from .models import AlumnoExamen
from alumno.models import Alumno
from examen_asignado.models import ExamenAsignado


class AlumnoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoExamen
        fields = '__all__'

class RegisterAlumnoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoExamen
        fields = '__all__'

    def create(self, validated_data):
        alumno_examen = AlumnoExamen.objects.create(
            alumno_id=validated_data['alumno_id'],
            examen_asignado_id=validated_data['examen_asignado_id'],
            fecha=validated_data['fecha'],
            calificacion=validated_data['calificacion']
        )
        return alumno_examen
    
class UpdateAlumnoExamenSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)

    class Meta:
        model = AlumnoExamen
        fields = '__all__'


class DeleteAlumnoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoExamen
        fields = '__all__'
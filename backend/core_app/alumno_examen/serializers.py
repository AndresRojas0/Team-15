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

class UpdateAlumnoExamenSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)

    class Meta:
        model = AlumnoExamen
        fields = '__all__'


class DeleteAlumnoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoExamen
        fields = '__all__'
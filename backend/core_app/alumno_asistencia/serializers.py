from rest_framework import serializers
from .models import AlumnoAsistencia
from curso.models import Curso
from alumno.models import Alumno

class AlumnoAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoAsistencia
        fields = '__all__'


class RegisterAlumnoAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoAsistencia
        fields = '__all__'

    def create(self, validated_data):
        alumno_asistencia = AlumnoAsistencia.objects.create(**validated_data)
        return alumno_asistencia
    

class UpdateAlumnoAsistenciaSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)
    curso_id= serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), required=False)
    alumno_id = serializers.PrimaryKeyRelatedField(queryset=Alumno.objects.all(), required=False)

    class Meta:
        model = AlumnoAsistencia
        fields = '__all__'
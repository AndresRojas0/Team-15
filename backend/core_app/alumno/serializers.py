from rest_framework import serializers
from .models import Alumno
from curso.models import Curso

class AlumnoSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Alumno
        fields = ['id', 'curso_id', 'nombre', 'apellido']

class RegisterAlumnoSerializer(serializers.Serializer):
    alumnos = AlumnoSerializer(many=True)

    def create(self, validated_data):
        alumnos_data = validated_data.pop('alumnos')
        alumnos = []
        for alumno_data in alumnos_data:
            alumno = Alumno.objects.create(**alumno_data)
            alumnos.append(alumno)
        return {'alumnos': alumnos}
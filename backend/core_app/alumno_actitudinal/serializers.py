from rest_framework import serializers
from .models import AlumnoActitudinal

class AlumnoActitudinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoActitudinal
        fields = '__all__'


class RegistroAlumnoActitudinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoActitudinal
        fields = '__all__'

    
class UpdateAlumnoActitudinalSerializer(serializers.ModelSerializer):
    alumno_id = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    curso_id = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    fecha = serializers.DateField(read_only=True, required=False)

    class Meta:
        model = AlumnoActitudinal
        fields = '__all__'
from rest_framework import serializers
from .models import AlumnoTarea

class AlumnoTareaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlumnoTarea
        fields = '__all__'

class RegistroAlumnoTareaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlumnoTarea
        fields = '__all__'


class UpdateAlumnoTareaSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)
    tipo_calificacion = serializers.CharField(required=False)

    class Meta:
        model = AlumnoTarea
        fields = '__all__'
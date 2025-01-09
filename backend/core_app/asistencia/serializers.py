from rest_framework import serializers
from asistencia.models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asistencia
        fields = '__all__'

class RegisterAsistenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asistencia
        fields = '__all__'
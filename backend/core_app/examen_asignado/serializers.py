from rest_framework import serializers
from examen_asignado.models import ExamenAsignado

class ExamenAsignadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamenAsignado
        fields = '__all__'


class RegisterExamenAsignadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamenAsignado
        fields = '__all__'

    def create(self, validated_data):
        examen_asignado = ExamenAsignado.objects.create(**validated_data)
        return examen_asignado
    

class UpdateExamenAsignadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamenAsignado
        fields = '__all__'

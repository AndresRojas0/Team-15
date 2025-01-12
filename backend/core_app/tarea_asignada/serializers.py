from rest_framework import serializers
from tarea_asignada.models import TareaAsignada

class TareaAsignadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaAsignada
        fields = '__all__'


class RegisterTareaAsignadaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TareaAsignada
        fields = '__all__'
from rest_framework import serializers
from planificacion_diaria.models import PlanificacionDiaria
from recurso_url.models import RecursoURL
from django.utils import timezone

class RecursoURLSerializer(serializers.ModelSerializer):
    planificacion_diaria_id = serializers.IntegerField(source='planificacion_diaria.id', read_only=True)
    fecha = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RecursoURL
        fields = ['url']
    
    def update(self, instance, validated_data):
        instance.fecha = timezone.now()
        return super().update(instance, validated_data)

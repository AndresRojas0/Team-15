from rest_framework import serializers

from subtema.models import Subtema
from .models import SubtemaAnual

class SubtemaAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtemaAnual
        fields = ['id', 'subtema_id', 'mes', 'año']


class UpdateSubtemaAnualSerializer(serializers.ModelSerializer):
    subtema_id = serializers.PrimaryKeyRelatedField(queryset=Subtema.objects.all())

    class Meta:
        model = SubtemaAnual
        fields = ['id', 'subtema_id', 'mes', 'año']

    def update(self, instance, validated_data):
        instance.subtema_id = validated_data.get('subtema_id', instance.subtema_id)
        instance.mes = validated_data.get('mes', instance.mes)
        instance.año = validated_data.get('año', instance.año)
        instance.save()
        return instance
    

class BulkSubtemaAnualSerializer(serializers.Serializer):
    subtemas_anuales = SubtemaAnualSerializer(many=True)

    def create(self, validated_data):
        subtemas_anuales_data = validated_data['subtemas_anuales']
        subtemas_anuales = [SubtemaAnual(**data) for data in subtemas_anuales_data]
        return SubtemaAnual.objects.bulk_create(subtemas_anuales)
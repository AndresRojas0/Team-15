from rest_framework import serializers

from subtema.models import Subtema
from .models import SubtemaAnual

class SubtemaAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtemaAnual
        fields = ['id', 'subtema_id', 'mes', 'año']


class UpdateSubtemaAnualSerializer(serializers.ModelSerializer):
    subtema_id = serializers.PrimaryKeyRelatedField(queryset=Subtema.objects.all(), required=False)
    año = serializers.IntegerField(required=False)

    class Meta:
        model = SubtemaAnual
        fields = '__all__'

class BulkSubtemaAnualSerializer(serializers.Serializer):
    subtemas_anuales = SubtemaAnualSerializer(many=True)

    def create(self, validated_data):
        subtemas_anuales_data = validated_data['subtemas_anuales']
        subtemas_anuales = [SubtemaAnual(**data) for data in subtemas_anuales_data]
        return SubtemaAnual.objects.bulk_create(subtemas_anuales)


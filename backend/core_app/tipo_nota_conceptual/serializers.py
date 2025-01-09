from rest_framework import serializers
from .models import TipoNotaConceptual

class TipoNotaConceptualSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNotaConceptual
        fields = '__all__'
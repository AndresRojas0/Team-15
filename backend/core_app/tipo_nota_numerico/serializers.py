from rest_framework import serializers
from tipo_nota_numerico.models import TipoNotaNumerico


class TipoNotaNumericoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNotaNumerico
        fields = '__all__'
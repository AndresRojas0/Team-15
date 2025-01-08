from rest_framework import serializers
from tipo_nota_binario.models import TipoNotaBinario

class TipoNotaBinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNotaBinario
        fields = '__all__'
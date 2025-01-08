from rest_framework import serializers
from tipo_nota_conceptual.serializers import TipoNotaConceptualSerializer
from tipo_nota_conceptual.models import TipoNotaConceptual
from tipo_nota_numerico.models import TipoNotaNumerico
from tipo_nota_numerico.serializers import TipoNotaNumericoSerializer
from tipo_nota_binario.models import TipoNotaBinario
from tipo_nota_binario.serializers import TipoNotaBinarioSerializer
from curso.models import Curso
from sistema_notas.models import SistemaNotas

class SistemaNotasSerializer(serializers.ModelSerializer):
    tipo_nota_numerico = TipoNotaNumericoSerializer(read_only=True)
    tipo_nota_binario = TipoNotaBinarioSerializer(read_only=True)
    tipo_nota_conceptual = TipoNotaConceptualSerializer(many=True, read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = SistemaNotas
        fields = ['id', 'curso_id', 'porcentaje_examenes', 'porcentaje_tareas', 'porcentaje_actitudinal', 'tipo_nota', 'tipo_nota_numerico', 'tipo_nota_binario', 'tipo_nota_conceptual']

class RegisterSistemaNotasSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')
    formato_nota = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = SistemaNotas
        fields = ['id', 'curso_id', 'porcentaje_examenes', 'porcentaje_tareas', 'porcentaje_actitudinal', 'tipo_nota', 'formato_nota']

    def create(self, validated_data):
        formato_nota_data = validated_data.pop('formato_nota', None)
        sistema_notas = SistemaNotas.objects.create(**validated_data)
        
        if validated_data['tipo_nota'] == 'numerico' and formato_nota_data:
            tipo_nota_numerico = TipoNotaNumerico.objects.create(**formato_nota_data)
            sistema_notas.tipo_nota_numerico = tipo_nota_numerico
        elif validated_data['tipo_nota'] == 'binario' and formato_nota_data:
            tipo_nota_binario = TipoNotaBinario.objects.create(**formato_nota_data)
            sistema_notas.tipo_nota_binario = tipo_nota_binario
        elif validated_data['tipo_nota'] == 'conceptual' and formato_nota_data:
            for nombre, valoracion in formato_nota_data.items():
                TipoNotaConceptual.objects.create(nombre=nombre, valoracion=valoracion, sistema_notas=sistema_notas)
        
        sistema_notas.save()
        return sistema_notas

    def to_representation(self, instance):
        serializer = SistemaNotasSerializer(instance)
        return serializer.data
from rest_framework import serializers
from asistencia.models import Asistencia
from asistencia.serializers import AsistenciaSerializer
from tipo_nota_conceptual.serializers import TipoNotaConceptualSerializer
from tipo_nota_conceptual.models import TipoNotaConceptual
from tipo_nota_numerico.models import TipoNotaNumerico
from tipo_nota_numerico.serializers import TipoNotaNumericoSerializer
from tipo_nota_binario.models import TipoNotaBinario
from tipo_nota_binario.serializers import TipoNotaBinarioSerializer
from curso.models import Curso
from sistema_notas.models import SistemaNotas

class SistemaNotasSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')
    formato_nota_tarea = serializers.SerializerMethodField()
    formato_actitudinal = TipoNotaConceptualSerializer(many=True, read_only=True)
    asistencia = AsistenciaSerializer()
    formato_nota_examen = serializers.SerializerMethodField()

    class Meta:
        model = SistemaNotas
        fields = ['id', 'curso_id', 'porcentaje_examenes', 'porcentaje_tareas', 'porcentaje_actitudinal', 'tipo_nota_tarea', 'formato_nota_tarea', 'tipo_nota_examen' , 'formato_nota_examen', 'formato_actitudinal', 'falta_justificada', 'asistencia']

    def get_formato_nota_tarea(self, instance):
        if instance.tipo_nota_tarea == 'numerico':
            return TipoNotaNumericoSerializer(instance.tipo_nota_numerico).data
        elif instance.tipo_nota_tarea == 'binario':
            return TipoNotaBinarioSerializer(instance.tipo_nota_binario).data
        elif instance.tipo_nota_tarea == 'conceptual':
            formato_nota_tarea = instance.tipo_nota_conceptual.filter(tipo='tarea')
            return TipoNotaConceptualSerializer(formato_nota_tarea, many=True).data
        return None
    
    def get_formato_nota_examen(self, instance):
        if instance.tipo_nota_examen == 'numerico':
            return TipoNotaNumericoSerializer(instance.examen_tipo_nota_numerico).data
        elif instance.tipo_nota_examen == 'binario':
            return TipoNotaBinarioSerializer(instance.examen_tipo_nota_binario).data
        elif instance.tipo_nota_examen == 'conceptual':
            formato_nota_examen = instance.tipo_nota_conceptual.filter(tipo='examen')
            return TipoNotaConceptualSerializer(formato_nota_examen, many=True).data


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formato_nota_tarea'] = self.get_formato_nota_tarea(instance)
        formato_actitudinal = instance.tipo_nota_conceptual.filter(tipo='actitudinal')
        representation['formato_actitudinal'] = TipoNotaConceptualSerializer(formato_actitudinal, many=True).data
        if instance.tipo_nota_examen:
            representation['formato_nota_examen'] = self.get_formato_nota_examen(instance)
        escala_asistencia = instance.tipo_nota_conceptual.filter(tipo='asistencia')
        representation['escala_asistencia'] = TipoNotaConceptualSerializer(escala_asistencia, many=True).data
        return representation

class RegisterSistemaNotasSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')
    formato_nota_tarea = serializers.JSONField(write_only=True, required=False)
    formato_nota_examen = serializers.JSONField(write_only=True, required=False)
    formato_actitudinal = serializers.JSONField(write_only=True, required=False)
    escala_asistencia = serializers.JSONField(write_only=True, required=False)
    asistencia = AsistenciaSerializer()


    class Meta:
        model = SistemaNotas
        fields = ['id', 'curso_id', 'porcentaje_examenes', 'porcentaje_tareas', 'porcentaje_actitudinal', 'tipo_nota_tarea', 'formato_nota_tarea', 'tipo_nota_examen', 'formato_nota_examen', 'formato_actitudinal', 'escala_asistencia', 'falta_justificada', 'asistencia']

    def create(self, validated_data):
        formato_nota_tarea_data = validated_data.pop('formato_nota_tarea', None)
        formato_nota_examen_data = validated_data.pop('formato_nota_examen', None)
        formato_actitudinal_data = validated_data.pop('formato_actitudinal', None)
        escala_asistencia_data = validated_data.pop('escala_asistencia', None)

        asistencia_data = validated_data.pop('asistencia')
        asistencia = Asistencia.objects.create(**asistencia_data)
        sistema_notas = SistemaNotas.objects.create(asistencia=asistencia, **validated_data)
        
        if validated_data.get('tipo_nota_tarea') == 'numerico' and formato_nota_tarea_data:
            tipo_nota_numerico = TipoNotaNumerico.objects.create(**formato_nota_tarea_data, es_un_examen=False)
            sistema_notas.tipo_nota_numerico = tipo_nota_numerico
        elif validated_data.get('tipo_nota_tarea') == 'binario' and formato_nota_tarea_data:
            tipo_nota_binario = TipoNotaBinario.objects.create(**formato_nota_tarea_data)
            sistema_notas.tipo_nota_binario = tipo_nota_binario
        elif validated_data.get('tipo_nota_tarea') == 'conceptual' and formato_nota_tarea_data:
            for nombre, valoracion in formato_nota_tarea_data.items():
                TipoNotaConceptual.objects.create(nombre=nombre, valoracion=valoracion, sistema_notas=sistema_notas, tipo='tarea')
        

        if validated_data.get('tipo_nota_examen') == 'numerico' and formato_nota_examen_data:
            examen_tipo_nota_numerico = TipoNotaNumerico.objects.create(**formato_nota_examen_data, es_un_examen=True)
            sistema_notas.examen_tipo_nota_numerico = examen_tipo_nota_numerico
        elif validated_data.get('tipo_nota_examen') == 'binario' and formato_nota_examen_data:
            examen_tipo_nota_binario = TipoNotaBinario.objects.create(**formato_nota_examen_data)
            sistema_notas.examen_tipo_nota_binario = examen_tipo_nota_binario
        elif validated_data.get('tipo_nota_examen') == 'conceptual' and formato_nota_examen_data:
            for nombre, valoracion in formato_nota_examen_data.items():
                TipoNotaConceptual.objects.create(nombre=nombre, valoracion=valoracion, sistema_notas=sistema_notas, tipo='examen')

        
        if formato_actitudinal_data:
            for nombre, valoracion in formato_actitudinal_data.items():
                TipoNotaConceptual.objects.create(nombre=nombre, valoracion=valoracion, sistema_notas=sistema_notas, tipo='actitudinal')
        
        if escala_asistencia_data:
            for nombre, valoracion in escala_asistencia_data.items():
                TipoNotaConceptual.objects.create(nombre=nombre, valoracion=valoracion, sistema_notas=sistema_notas, tipo='asistencia')

        sistema_notas.save()
        return sistema_notas

    def get_formato_nota_tarea(self, instance):
        if instance.tipo_nota_tarea == 'numerico':
            return TipoNotaNumericoSerializer(instance.tipo_nota_numerico).data
        elif instance.tipo_nota_tarea == 'binario':
            return TipoNotaBinarioSerializer(instance.tipo_nota_binario).data
        elif instance.tipo_nota_tarea == 'conceptual':
            formato_nota_tarea = instance.tipo_nota_conceptual.filter(tipo='tarea')
            return TipoNotaConceptualSerializer(formato_nota_tarea, many=True).data
        return None

    def get_formato_nota_examen(self, instance):
        if instance.tipo_nota_examen == 'numerico':
            return TipoNotaNumericoSerializer(instance.examen_tipo_nota_numerico).data
        elif instance.tipo_nota_examen == 'binario':
            return TipoNotaBinarioSerializer(instance.examen_tipo_nota_binario).data
        elif instance.tipo_nota_examen == 'conceptual':
            formato_nota_examen = instance.tipo_nota_conceptual.filter(tipo='examen')
            return TipoNotaConceptualSerializer(formato_nota_examen, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['formato_nota_tarea'] = self.get_formato_nota_tarea(instance)
        formato_actitudinal = instance.tipo_nota_conceptual.filter(tipo='actitudinal')
        representation['formato_actitudinal'] = TipoNotaConceptualSerializer(formato_actitudinal, many=True).data
        representation['formato_nota_examen'] = self.get_formato_nota_examen(instance)
        escala_asistencia = instance.tipo_nota_conceptual.filter(tipo='asistencia')
        representation['escala_asistencia'] = TipoNotaConceptualSerializer(escala_asistencia, many=True).data
        return representation
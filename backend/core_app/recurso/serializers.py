from rest_framework import serializers
from curso.models import Curso
from .models import Recurso

class RecursoSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Recurso
        fields = ['id', 'curso_id', 'nombre', 'descripcion', 'url']

class RegisterRecursoSerializer(serializers.Serializer):
    recursos = RecursoSerializer(many=True)

    def create(self, validated_data):
        recursos_data = validated_data.pop('recursos')
        recursos = []
        for recurso_data in recursos_data:
            recurso = Recurso.objects.create(**recurso_data)
            recursos.append(recurso)
        return {'recursos': recursos}
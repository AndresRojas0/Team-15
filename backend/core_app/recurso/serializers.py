from rest_framework import serializers
from curso.models import Curso
from .models import Recurso

class RecursoSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Recurso
        fields = ['id', 'curso_id', 'nombre', 'descripcion', 'url']

class RegisterRecursoSerializer(serializers.ModelSerializer):
    curso_id = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all(), source='curso')

    class Meta:
        model = Recurso
        fields = ['curso_id', 'nombre', 'descripcion', 'url']

    def validate(self, data):
        curso_id = data.get('curso')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        url = data.url('url')
        if not curso_id:
            raise serializers.ValidationError("Course ID is required")
        if not nombre:
            raise serializers.ValidationError("Name is required")
        return data
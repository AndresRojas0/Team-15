# filepath: /c:/Users/crist/Desktop/Foo Talent Group/Team-15/backend/core_app/curso/serializers.py
from rest_framework import serializers
from alumno.serializers import AlumnoSerializer
from alumno_asistencia.serializers import AlumnoAsistenciaSerializer
from institucion.models import Institucion
from sistema_notas.serializers import SistemaNotasSerializer
from periodo.models import Periodo
from periodo.serializers import PeriodoSerializer
from materia.serializers import MateriaSerializer
from .models import Curso

class CursoSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)
    periodos = PeriodoSerializer(many=True, read_only=True)
    sistema_notas = SistemaNotasSerializer(many=True, read_only=True)
    alumnos = AlumnoSerializer(many=True, read_only=True)
    alumno_asistencia = AlumnoAsistenciaSerializer(many=True, read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'institucion_id', 'nombre', 'duracion', 'periodos', 'materias', 'sistema_notas', 'alumnos', 'alumno_asistencia']


class UpdateCursoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    institucion_id = serializers.PrimaryKeyRelatedField(queryset=Institucion.objects.all(), required=False)

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'institucion_id', 'duracion']
        read_only_fields = ['id', 'institucion_id', 'duracion']

class RegisterCursoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    institucion_id = serializers.IntegerField(required=True)
    periodos = PeriodoSerializer(many=True, write_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'institucion_id', 'duracion', 'periodos']

    def create(self, validated_data):
        periodos_data = validated_data.pop('periodos')
        curso = Curso.objects.create(**validated_data)
        for periodo_data in periodos_data:
            Periodo.objects.create(curso=curso, **periodo_data)
        return curso

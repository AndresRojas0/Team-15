from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alumno
from .serializers import AlumnoSerializer, RegisterAlumnoSerializer
from curso.models import Curso
from institucion.models import Institucion
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

logger = logging.getLogger(__name__)

class RegisterAlumnosView(generics.CreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = RegisterAlumnoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            alumnos = serializer.save()
            return Response({
                'alumnos': AlumnoSerializer(alumnos['alumnos'], many=True).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListAlumnoView(generics.ListAPIView):
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Alumno.objects.filter(curso__in=cursos)
    

class ProcessAlumnoExcelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            curso_id = request.data.get('curso_id')
            if not curso_id:
                return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            df = pd.read_excel(file)
            alumnos = []
            for _, row in df.iterrows():
                nombre = row['nombre']
                apellido = row['apellido']
                alumno_data = {
                    'curso_id': curso_id,
                    'nombre': nombre,
                    'apellido': apellido
                }
                alumnos.append(alumno_data)
            return Response({
                'alumnos': alumnos
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterAlumnoView(generics.CreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = RegisterAlumnoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            alumno = serializer.save()
            return Response({
                'alumno': AlumnoSerializer(alumno).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
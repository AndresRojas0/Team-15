from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Planificacion
from .serializers import PlanificacionSerializer, RegisterPlanificacionSerializer
from curso.models import Curso
from institucion.models import Institucion
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

logger = logging.getLogger(__name__)

class RegisterPlanificacionView(generics.CreateAPIView):
    queryset = Planificacion.objects.all()
    serializer_class = RegisterPlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            planificaciones = serializer.save()
            return Response({
                'planificaciones': PlanificacionSerializer(planificaciones['planificaciones'], many=True).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListPlanificacionView(generics.ListAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Planificacion.objects.filter(curso__in=cursos)
    

class ProcessPlanificacionExcelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            curso_id = request.data.get('curso_id')
            if not curso_id:
                return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            df = pd.read_excel(file)
            planificaciones = []
            for _, row in df.iterrows():
                tipo = row['tipo']
                contenido = row['contenido']
                metodologia = row['metodologia']
                anotaciones = row['anotaciones']
                planificacion_data = {
                    'curso_id': curso_id,
                    'tipo': tipo,
                    'contenido': contenido,
                    'metodologia': metodologia,
                    'anotaciones': anotaciones
                }
                planificaciones.append(planificacion_data)
            return Response({
                'planificaciones': planificaciones
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


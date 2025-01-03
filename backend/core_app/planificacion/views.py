from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Planificacion
from .serializers import PlanificacionSerializer, RegisterPlanificacionSerializer
from curso.models import Curso
from materia.models import Materia
from institucion.models import Institucion
import logging
from rest_framework.parsers import MultiPartParser, FormParser

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
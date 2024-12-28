from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Seguimiento
from .serializers import SeguimientoSerializer, RegisterSeguimientoSerializer
from curso.models import Curso
from alumno.models import Alumno
from institucion.models import Institucion
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd

logger = logging.getLogger(__name__)

class RegisterSeguimientoView(generics.CreateAPIView):
    queryset = Seguimiento.objects.all()
    serializer_class = RegisterSeguimientoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            seguimientos = serializer.save()
            return Response({
                'seguimientos': SeguimientoSerializer(seguimientos['seguimientos'], many=True).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListSeguimientoView(generics.ListAPIView):
    serializer_class = SeguimientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Seguimiento.objects.filter(curso__in=cursos)

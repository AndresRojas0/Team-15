from tokenize import TokenError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from curso.models import Curso
from .models import Recurso
from .serializers import RecursoSerializer, RegisterRecursoSerializer
from django.db import IntegrityError

class RegisterRecursosView(generics.CreateAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RegisterRecursoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            recursos = serializer.save()
            return Response({
                'recursos': RecursoSerializer(recursos['recursos'], many=True).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListRecursoView(generics.ListAPIView):
    serializer_class = RecursoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Recurso.objects.filter(curso__in=cursos)

class RegisterRecursoView(generics.CreateAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RegisterRecursoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            recurso = serializer.save()
            return Response({
                'recurso': RecursoSerializer(recurso).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
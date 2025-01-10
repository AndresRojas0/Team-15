from tokenize import TokenError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from curso.models import Curso
from .models import Recurso
from .serializers import RecursoSerializer, RegisterRecursoSerializer
from django.db import IntegrityError


class RegisterRecursoView(generics.CreateAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RegisterRecursoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return Response({'error': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid authorization header format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access = AccessToken(token)
            user_id = access['user_id']
        except TokenError:
            return Response({'error': 'Token is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data.copy()
        curso_id = data.get('curso_id')
        if not curso_id:
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            curso = Curso.objects.get(id=curso_id, institucion__docente_id=user_id)
        except Curso.DoesNotExist:
            return Response({'error': 'Course not found or you do not have permission to add a resource to this course'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            recurso = serializer.save()
        except IntegrityError:
            return Response({'error': 'A resource with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'recurso': RecursoSerializer(recurso).data
        }, status=status.HTTP_201_CREATED)
    

class ListRecursoView(generics.ListAPIView):
    serializer_class = RecursoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recurso.objects.filter(curso__institucion__docente=user)


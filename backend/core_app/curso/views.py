from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from .models import Curso
from .serializers import CursoSerializer, RegisterCursoSerializer, UpdateCursoSerializer
from institucion.models import Institucion
from django.db import IntegrityError 
from rest_framework.exceptions import PermissionDenied

class RegisterCursoView(generics.CreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = RegisterCursoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UpdateCursoView(generics.UpdateAPIView):
    queryset = Curso.objects.all()
    serializer_class = UpdateCursoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.institucion.docente != request.user:
            raise PermissionDenied('No tienes permiso para modificar este curso')
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)        
    

class ListCursoView(generics.ListAPIView):
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Curso.objects.filter(institucion__docente=user)
    

class DeleteCursoView(generics.DestroyAPIView):
    queryset = Curso.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
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
        
        curso_id = kwargs.get('pk')
        if not curso_id:
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if curso.institucion.docente_id != user_id:
            return Response({'error': 'No tienes permiso para eliminar este curso'}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(curso)
        return Response(status=status.HTTP_204_NO_CONTENT)
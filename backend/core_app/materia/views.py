# filepath: /c:/Users/crist/Desktop/Foo Talent Group/Team-15/backend/core_app/materia/views.py
from tokenize import TokenError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from curso.models import Curso
from .models import Materia
from .serializers import DeleteSerializer, MateriaSerializer, RegisterMateriaSerializer, UpdateSerializer
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied


class RegisterMateriaView(generics.CreateAPIView):
    queryset = Materia.objects.all()
    serializer_class = RegisterMateriaSerializer
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
            return Response({'error': 'Course not found or you do not have permission to add a subject to this course'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            materia = serializer.save()
        except IntegrityError:
            return Response({'error': 'A subject with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'materia': MateriaSerializer(materia).data
        }, status=status.HTTP_201_CREATED)
    

class ListMateriaView(generics.ListAPIView):
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Materia.objects.filter(curso__institucion__docente=user)


class UpdateMateriaView(generics.UpdateAPIView):
    queryset = Materia.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.curso.institucion.docente != request.user:
            raise PermissionDenied('No tienes permiso para realizar esta acción.')
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class DeleteMateriaView(generics.DestroyAPIView):
    queryset = Materia.objects.all()
    serializer_class = DeleteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.curso.institucion.docente != request.user:
            raise PermissionDenied('No tienes permiso para realizar esta acción.')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
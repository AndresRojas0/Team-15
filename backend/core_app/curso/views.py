from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from .models import Curso
from .serializers import CursoSerializer, RegisterCursoSerializer, UpdateCursoSerializer
from institucion.models import Institucion
from django.db import IntegrityError 

class RegisterCursoView(generics.CreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = RegisterCursoSerializer
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
        institucion_id = data.get('institucion_id')
        if not institucion_id:
            return Response({'error': 'Institution ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            institucion = Institucion.objects.get(id=institucion_id, docente_id=user_id)
        except Institucion.DoesNotExist:
            return Response({'error': 'Institution not found or you do not have permission to add a course to this institution'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            curso = serializer.save()
        except IntegrityError:
            return Response({'error': 'A course with this name already exists for this institution'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'curso': CursoSerializer(curso).data
        }, status=status.HTTP_201_CREATED)
    

class UpdateCursoView(generics.UpdateAPIView):
    queryset = Curso.objects.all()
    serializer_class = UpdateCursoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
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
        
        curso_id = request.data.get('id')
        if not curso_id:
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if curso.institucion.docente_id != user_id:
            return Response({'error': 'You do not have permission to update this course'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        serializer = self.get_serializer(curso, data=data, partial=False)  # partial=False to require all fields
        try:
            serializer.is_valid(raise_exception=True)
            curso = serializer.save()
        except IntegrityError:
            return Response({'error': 'A course with this name already exists for this institution'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'curso': CursoSerializer(curso).data
        }, status=status.HTTP_200_OK)
    

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
            return Response({'error': 'You do not have permission to delete this course'}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(curso)
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from alumno_actitudinal.serializers import AlumnoActitudinalSerializer, RegistroAlumnoActitudinalSerializer, UpdateAlumnoActitudinalSerializer
from alumno_actitudinal.models import AlumnoActitudinal
from rest_framework import viewsets


class RegisterAlumnoActitudinal(generics.CreateAPIView):
    serializer_class = RegistroAlumnoActitudinalSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ListAlumnoActitudinal(generics.ListAPIView):
    queryset = AlumnoActitudinal.objects.all()
    serializer_class = AlumnoActitudinalSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = AlumnoActitudinal.objects.filter(curso_id__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)


class UpdateAlumnoActitudinal(viewsets.ModelViewSet):
    queryset = AlumnoActitudinal.objects.all()
    serializer_class = AlumnoActitudinalSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.curso_id.institucion.docente != request.user:
            raise PermissionDenied()
        data = request.data
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.curso_id.institucion.docente != request.user:
            raise PermissionDenied()
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class DeleteAlumnoActitudinal(generics.DestroyAPIView):
    queryset = AlumnoActitudinal.objects.all()
    serializer_class = AlumnoActitudinalSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        # Verificar que el usuario autenticado tiene permiso para eliminar el registro
        if instance.curso_id.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar esta asistencia")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

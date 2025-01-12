from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from alumno_examen.serializers import AlumnoExamenSerializer, DeleteAlumnoExamenSerializer, RegisterAlumnoExamenSerializer, UpdateAlumnoExamenSerializer
from .models import AlumnoExamen
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class RegisterAlumnoExamenView(generics.CreateAPIView):
    serializer_class = RegisterAlumnoExamenSerializer
    queryset = AlumnoExamen.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListAlumnoExamenView(generics.ListAPIView):
    queryset = AlumnoExamen.objects.all()
    serializer_class = AlumnoExamenSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = AlumnoExamen.objects.filter(examen_asignado_id__materia_id__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)
    
    
# CUALQUIER USUARIO PUEDE MODIFICAR CUALQUIER REGISTRO Y ESO NO DEBERÍA SER ASÍ!
class UpdateAlumnoExamenView(generics.UpdateAPIView):
    queryset = AlumnoExamen.objects.all()
    serializer_class = UpdateAlumnoExamenSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.examen_asignado_id.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este examen")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DeleteAlumnoExamenView(generics.DestroyAPIView):
    queryset = AlumnoExamen.objects.all()
    serializer_class = AlumnoExamenSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.examen_asignado_id.materia_id.curso.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar este examen")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
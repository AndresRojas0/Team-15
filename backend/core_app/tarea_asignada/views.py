from django.shortcuts import render
from tarea_asignada.models import TareaAsignada
from tarea_asignada.serializers import TareaAsignadaSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterTareaAsignadaViewSet(viewsets.ModelViewSet):
    queryset = TareaAsignada.objects.all()
    serializer_class = TareaAsignadaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ListTareaAsignadaViewSet(viewsets.ModelViewSet):
    queryset = TareaAsignada.objects.all()
    serializer_class = TareaAsignadaSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = TareaAsignada.objects.filter(materia_id__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)
    
class UpdateTareaAsignadaViewSet(viewsets.ModelViewSet):
    queryset = TareaAsignada.objects.all()
    serializer_class = TareaAsignadaSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar esta tarea")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DeleteTareaAsignadaViewSet(viewsets.ModelViewSet):
    queryset = TareaAsignada.objects.all()
    serializer_class = TareaAsignadaSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para eliminar esta tarea")
        instance.delete()
        return Response("Tarea eliminada", status=status.HTTP_204_NO_CONTENT)
from django.shortcuts import render
from .models import Subtema
from .serializers import SubtemaSerializer, RegisterSubtemaSerializer, UpdateSubtemaSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from planificacion.models import Planificacion
from tema.models import Tema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class ListAllSubtemasView(generics.ListAPIView):
    serializer_class = SubtemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        planificaciones = Planificacion.objects.filter(materia__curso__institucion__docente_id=user_id)
        temas = Tema.objects.filter(id_planificacion__in=planificaciones)
        return Subtema.objects.filter(id_tema__in=temas)
    

class RegisterSubtemaView(generics.CreateAPIView):
    queryset = Subtema.objects.all()
    serializer_class = RegisterSubtemaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = RegisterSubtemaSerializer(data=request.data)
        if serializer.is_valid():
            subtema = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# UPDATE PERMITE QUE CUALQUIER USUARIO PUEDA MODIFICAR CUALQUIER SUBTEMA Y NO DEBERIA SER ASI
class UpdateSubtemaView(generics.UpdateAPIView):
    queryset = Subtema.objects.all()
    serializer_class = UpdateSubtemaSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id_tema.id_planificacion.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este subtema")
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class DeleteSubtemaView(generics.DestroyAPIView):
    queryset = Subtema.objects.all()
    serializer_class = SubtemaSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.id_tema.id_planificacion.materia.curso.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar este subtema")
        instance.delete()
        return Response("Subtema eliminado", status=status.HTTP_204_NO_CONTENT)
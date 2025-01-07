from django.shortcuts import render
from .models import Subtema
from .serializers import SubtemaSerializer, RegisterSubtemaSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from planificacion.models import Planificacion
from tema.models import Tema
from rest_framework import status
from rest_framework.response import Response


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
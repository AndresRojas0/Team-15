from django.shortcuts import render
from .models import Subtema
from .serializers import SubtemaSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from planificacion.models import Planificacion
from tema.models import Tema


class ListAllSubtemasView(generics.ListAPIView):
    serializer_class = SubtemaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        planificaciones = Planificacion.objects.filter(materia__curso__institucion__docente_id=user_id)
        temas = Tema.objects.filter(id_planificacion__in=planificaciones)
        return Subtema.objects.filter(id_tema__in=temas)
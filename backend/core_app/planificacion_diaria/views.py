from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from planificacion_diaria.models import PlanificacionDiaria
from planificacion_diaria.serializers import PlanificacionDiariaCreateSerializer, PlanificacionDiariaSerializer, UpdatePlanificacionDiariaSerializer


class RegisterPlanificacionDiariaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        serializer = PlanificacionDiariaCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListPlanificacionDiariaViewSet(viewsets.ModelViewSet):
    queryset = PlanificacionDiaria.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PlanificacionDiariaSerializer

    def list(self, request):
        user = self.request.user
        queryset = PlanificacionDiaria.objects.filter(planificacion_id__materia__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)
    

class UpdatePlanificacionDiaria(viewsets.ModelViewSet):
    queryset = PlanificacionDiaria.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePlanificacionDiariaSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.planificacion_id.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar esta planificación")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DeletePlanificacionDiaria(viewsets.ModelViewSet):
    queryset = PlanificacionDiaria.objects.all()
    serializer_class = PlanificacionDiariaSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.planificacion_id.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para eliminar esta planificación")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
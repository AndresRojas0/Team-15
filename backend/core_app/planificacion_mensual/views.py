from planificacion_mensual.models import PlanificacionMensual
from planificacion_mensual.serializers import PlanificacionMensualSerializer, UpdatePlanificacionMensualSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class PlanificacionMensualView(generics.CreateAPIView):
    serializer_class = PlanificacionMensualSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'planificacion_mensual': serializer.data
        }, status=status.HTTP_201_CREATED)



class PlanificacionMensualBulkView(generics.CreateAPIView):
    serializer_class = PlanificacionMensualSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'planificacion_mensual': serializer.data
        }, status=status.HTTP_201_CREATED)
    
class ListPlanificacionMensualView(generics.ListAPIView):
    serializer_class = PlanificacionMensualSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PlanificacionMensual.objects.filter(planificacion_id__materia__curso__institucion__docente=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'planificacion_mensual': serializer.data
        }, status=status.HTTP_200_OK)


class UpdatePlanificacionMensualView(generics.UpdateAPIView):
    queryset = PlanificacionMensual.objects.all()
    serializer_class = UpdatePlanificacionMensualSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.planificacion_id.materia.curso.institucion.docente != request.user:
            raise PermissionDenied('No tienes permiso para realizar esta acción.')
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DeletePlanificacionMensualView(generics.DestroyAPIView):
    queryset = PlanificacionMensual.objects.all()
    serializer_class = PlanificacionMensualSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.planificacion_id.materia.curso.institucion.docente != request.user:
            raise PermissionDenied('No tienes permiso para realizar esta acción.')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
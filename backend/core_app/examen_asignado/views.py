from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from examen_asignado.models import ExamenAsignado
from examen_asignado.serializers import ExamenAsignadoSerializer, RegisterExamenAsignadoSerializer, UpdateExamenAsignadoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class RegisterExamenAsignadoViewSet(viewsets.ViewSet):
    queryset = ExamenAsignado.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = RegisterExamenAsignadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class ListExamenAsignadoViewSet(viewsets.ModelViewSet):
    queryset = ExamenAsignado.objects.all()
    serializer_class = ExamenAsignadoSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = ExamenAsignado.objects.filter(materia_id__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)
    


class UpdateExamenAsignadoViewSet(viewsets.ModelViewSet):
    queryset = ExamenAsignado.objects.all()
    serializer_class = UpdateExamenAsignadoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este examen")
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este examen")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DeleteExamenAsignadoViewSet(viewsets.ModelViewSet):
    queryset = ExamenAsignado.objects.all()
    serializer_class = ExamenAsignadoSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        # Verificar que el usuario autenticado tiene permiso para eliminar el registro
        if instance.materia_id.curso.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar este examen")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

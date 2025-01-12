from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SubtemaAnual
from .serializers import SubtemaAnualSerializer, UpdateSubtemaAnualSerializer, BulkSubtemaAnualSerializer
from rest_framework.exceptions import PermissionDenied

class SubtemaAnualViewSet(viewsets.ModelViewSet):
    queryset = SubtemaAnual.objects.all()
    serializer_class = SubtemaAnualSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = SubtemaAnualSerializer(data=request.data)
        if serializer.is_valid():
            subtema_anual = serializer.save()
            return Response(SubtemaAnualSerializer(subtema_anual).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BulkCreateSubtemaAnualView(generics.CreateAPIView):
    queryset = SubtemaAnual.objects.all()
    serializer_class = BulkSubtemaAnualSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subtemas_anuales = serializer.save()
        return Response(SubtemaAnualSerializer(subtemas_anuales, many=True).data, status=status.HTTP_201_CREATED)
    

class ListSubtemaAnualView(generics.ListAPIView):
    queryset = SubtemaAnual.objects.all()
    serializer_class = SubtemaAnualSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return SubtemaAnual.objects.filter(subtema_id__id_tema__id_planificacion__materia__curso__institucion__docente_id=user_id)
    

class UpdateSubtemaAnualView(generics.UpdateAPIView):
    queryset = SubtemaAnual.objects.all()
    serializer_class = UpdateSubtemaAnualSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.subtema_id.id_tema.id_planificacion.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este subtema")
        data = request.data
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class DeleteSubtemaAnualView(generics.DestroyAPIView):
    queryset = SubtemaAnual.objects.all()
    serializer_class = SubtemaAnualSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.subtema_id.id_tema.id_planificacion.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este subtema")
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
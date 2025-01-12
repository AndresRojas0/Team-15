from alumno_tarea.models import AlumnoTarea
from alumno_tarea.serializers import AlumnoTareaSerializer, RegistroAlumnoTareaSerializer, UpdateAlumnoTareaSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RegisterAlumnoTarea(generics.CreateAPIView):
    queryset = AlumnoTarea.objects.all()
    serializer_class = RegistroAlumnoTareaSerializer
    permission_classes = [IsAuthenticated]

    def create (self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListAlumnoTarea(generics.ListAPIView):
    queryset = AlumnoTarea.objects.all()
    serializer_class = AlumnoTareaSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = AlumnoTarea.objects.filter(tarea_asignada_id__materia_id__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)


# CUALQUIER USUARIO PUEDE MODIFICAR CUALQUIER REGISTRO Y ESO NO DEBERÍA SER ASÍ
class UpdateAlumnoTarea(generics.UpdateAPIView):
    queryset = AlumnoTarea.objects.all()
    serializer_class = UpdateAlumnoTareaSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.tarea_asignada_id.materia_id.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar este registro")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class DeleteAlumnoTarea(generics.DestroyAPIView):
    queryset = AlumnoTarea.objects.all()
    serializer_class = AlumnoTareaSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        # Verificar que el usuario autenticado tiene permiso para eliminar el registro
        if instance.tarea_asignada_id.materia_id.curso.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar este registro")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
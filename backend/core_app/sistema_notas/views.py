from rest_framework import viewsets, generics
from .models import SistemaNotas
from .serializers import SistemaNotasSerializer, RegisterSistemaNotasSerializer
from rest_framework.permissions import IsAuthenticated

class SistemaNotasViewSet(viewsets.ModelViewSet):
    queryset = SistemaNotas.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RegisterSistemaNotasSerializer
        return SistemaNotasSerializer


class ListSistemaNotasViewSet(generics.ListAPIView):
    serializer_class = SistemaNotasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SistemaNotas.objects.filter(curso__institucion__docente=user)

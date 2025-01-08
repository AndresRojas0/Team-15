from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SubtemaAnual
from .serializers import SubtemaAnualSerializer, UpdateSubtemaAnualSerializer, BulkSubtemaAnualSerializer

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
    
    def update(self, request, pk=None):
        subtema_anual = SubtemaAnual.objects.get(id=pk)
        serializer = UpdateSubtemaAnualSerializer(subtema_anual, data=request.data, partial=True)
        if serializer.is_valid():
            subtema_anual = serializer.save()
            return Response(SubtemaAnualSerializer(subtema_anual).data, status=status.HTTP_200_OK)
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
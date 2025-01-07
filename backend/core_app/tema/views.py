from rest_framework import viewsets
from .models import Tema
from .serializers import RegisterOnlyTemaSerializer, TemaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_temas(self, request):
        user = request.user
        temas = Tema.objects.filter(user=user)
        serializer = TemaSerializer(temas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = RegisterOnlyTemaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = RegisterOnlyTemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


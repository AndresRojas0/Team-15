from django.shortcuts import render
from rest_framework import viewsets
from tipo_nota_numerico.models import TipoNotaNumerico
from tipo_nota_numerico.serializers import TipoNotaNumericoSerializer
from rest_framework.permissions import IsAuthenticated

class ListAllTipoNotaNumericoView(viewsets.ModelViewSet):
    queryset = TipoNotaNumerico.objects.all()
    serializer_class = TipoNotaNumericoSerializer
    
    
class ListTipoNotaNumericaAuth(viewsets.ModelViewSet):
    queryset = TipoNotaNumerico.objects.all()
    serializer_class = TipoNotaNumericoSerializer
    permission_classes = [IsAuthenticated]
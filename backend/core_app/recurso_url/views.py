import uuid
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from django.conf import settings
from google.cloud import storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import AccessToken, TokenError

from recurso_url.serializers import RecursoURLSerializer
from recurso_url.models import RecursoURL
from rest_framework.response import Response
from rest_framework.views import APIView


class RecursoURLView(APIView):
    serializer_class = RecursoURLSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        request.user = RecursoURL.objects.first()
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
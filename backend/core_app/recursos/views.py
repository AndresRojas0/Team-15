import uuid
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from planificacion_diaria.models import PlanificacionDiaria
from .serializers import RecursoSerializer, RegisterRecursoSerializer
from recursos.models import Recurso
from django.conf import settings
from google.cloud import storage
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import AccessToken, TokenError


class RegistrarRecursoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = RegisterRecursoSerializer

    def post(self, request, *args, **kwargs):
        try:
            archivo = request.data.get('archivo')

            auth_header = request.headers.get('Authorization')
            token_type, token = auth_header.split()
            access = AccessToken(token)
            usuario_id = access['user_id'] 
            carpeta_usuario = f"recursos/{usuario_id}/"
            guid = str(uuid.uuid4())
            # Obtener la extensión del archivo (como .pdf, .jpg, etc.)
            extension = archivo.name.split('.')[-1]
            nuevo_nombre = f"{guid}.{extension}"

            url = self.subir_a_google_cloud(archivo, carpeta_usuario, nuevo_nombre)
            data = request.data.copy()
            data['url'] = url

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            recurso = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except TokenError:
            raise PermissionDenied("Token inválido o expirado")
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    def subir_a_google_cloud(self, archivo, carpeta_usuario, nuevo_nombre):
        # Crear el cliente de Google Cloud Storage
        client = storage.Client()
        bucket = client.get_bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET)

        ruta_archivo = f"{carpeta_usuario}{nuevo_nombre}"

        # Detectar el tipo MIME (por ejemplo, 'image/jpeg', 'image/png', etc.)
        import mimetypes
        tipo_mime, _ = mimetypes.guess_type(archivo.name)

        blob = bucket.blob(ruta_archivo)
        blob.upload_from_file(archivo.file, content_type=tipo_mime)

        # Generar la URL pública automáticamente sin configurar ACLs
        return blob.public_url
    

class ListRecursosViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RecursoSerializer

    def list(self, request):
        user = self.request.user
        queryset = Recurso.objects.filter(planificacion_diaria_id__planificacion_id__materia__curso__institucion__docente=user)
        return Response(self.get_serializer(queryset, many=True).data)
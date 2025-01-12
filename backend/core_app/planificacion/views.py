from io import BytesIO
from django.conf import settings
import docx
import pdfplumber
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Planificacion
from .serializers import DeletePlanificacionSerializer, PlanificacionSerializer, RegisterPlanificacionSerializer, UpdatePlanificacionSerializer
from curso.models import Curso
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import json
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class RegisterPlanificacionView(generics.CreateAPIView):
    queryset = Planificacion.objects.all()
    serializer_class = RegisterPlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            planificacion = serializer.save()
            return Response({
                'planificacion': PlanificacionSerializer(planificacion, context=self.get_serializer_context()).data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"ValidationError occurred: {e}")
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListPlanificacionView(generics.ListAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Planificacion.objects.filter(materia__curso__in=cursos)



class WordFileProcessor(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No se ha subido ningún archivo."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']

        try:
            doc = docx.Document(BytesIO(uploaded_file.read()))

            # Extraer todo el contenido del documento
            content = '\n'.join([para.text.strip() for para in doc.paragraphs])

            chat_session = settings.MODEL.start_chat(history=[])
            response = chat_session.send_message(
                f"Por favor, extrae los temas y subtemas de APRENDIZAJES Y CONTENIDOS del siguiente texto:\n{content}\n"
                "Responde en formato JSON con la siguiente estructura: "
                '{"temas": [{"tema": "nombre_tema", "subtemas": ["subtema1", "subtema2", ...] }, {...}]}'
            )

            # Respuesta de la API
            response_text = response.text

            # Limpiar la respuesta de las marcas de bloque de código
            # Elimina el marcador de inicio y fin del bloque de código
            if response_text.startswith("```json"):
                response_text = response_text[7:].strip()  # Eliminar "```json\n"
            if response_text.endswith("```"):
                response_text = response_text[:-3].strip()  # Eliminar "```"

            try:
                json_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"Error de parseo JSON: {e}")  # Depuración
                return Response(
                    {"error": "La respuesta de la API no es un JSON válido."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(json_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PDFExtractTextView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No se ha subido ningún archivo PDF."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']

        try:
            text = self.extract_pdf_text(uploaded_file)

            chat_session = settings.MODEL.start_chat(history=[])
            response = chat_session.send_message(
                f"Por favor, extrae los temas y subtemas de APRENDIZAJES Y CONTENIDOS del siguiente texto:\n{text}\n"
                "Responde en formato JSON con la siguiente estructura: "
                '{"temas": [{"tema": "nombre_tema", "subtemas": ["subtema1", "subtema2", ...] }, {...}]}'
            )

            response_text = response.text
            
            if response_text.startswith("```json"):
                response_text = response_text[7:].strip()
            if response_text.endswith("```"):
                response_text = response_text[:-3].strip()

            try:
                json_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                return Response(
                    {"error": "La respuesta de la API no es un JSON válido."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(json_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_pdf_text(self, pdf_file):
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()  # Extraemos el texto de cada página
        return text
    

class UpdatePlanificacionView(generics.UpdateAPIView):
    queryset = Planificacion.objects.all()
    serializer_class = UpdatePlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.materia.curso.institucion.docente != request.user:
            raise PermissionDenied("No tienes permiso para modificar esta planificación")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DeletePlanificacionView(generics.DestroyAPIView):
    queryset = Planificacion.objects.all()
    serializer_class = DeletePlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.materia.curso.institucion.docente != user:
            raise PermissionDenied("No tienes permiso para eliminar esta planificación")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
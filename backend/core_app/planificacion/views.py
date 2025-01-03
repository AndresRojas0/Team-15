from io import BytesIO
import os
from xml.dom.minidom import Document
from django.conf import settings
import docx
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Planificacion
from .serializers import PlanificacionSerializer, RegisterPlanificacionSerializer
from curso.models import Curso
from materia.models import Materia
from institucion.models import Institucion
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import google.generativeai as genai

logger = logging.getLogger(__name__)

class RegisterPlanificacionView(generics.CreateAPIView):
    queryset = Planificacion.objects.all()
    serializer_class = RegisterPlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            planificaciones = serializer.save()
            return Response({
                'planificaciones': PlanificacionSerializer(planificaciones['planificaciones'], many=True).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response({'error': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListPlanificacionView(generics.ListAPIView):
    serializer_class = PlanificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cursos = Curso.objects.filter(institucion__docente_id=user_id)
        return Planificacion.objects.filter(curso__in=cursos)
        
        

class WordFileProcessor(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No se ha subido ningún archivo."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES['file']

        try:
            doc = docx.Document(BytesIO(uploaded_file.read()))

            # Extraer texto de la sección "APRENDIZAJES Y CONTENIDOS"
            content = self.extract_relevant_content(doc)

            if not content:
                return Response({"error": "No se encontró la sección 'APRENDIZAJES Y CONTENIDOS' en el documento."}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Enviar el texto extraído a la API de Gemini para obtener temas y subtemas
            chat_session = settings.MODEL.start_chat(history=[])
            response = chat_session.send_message(f"Por favor, extrae los temas y subtemas de APRENDIZAJES Y CONTENIDOS del siguiente texto:\n{content}")

            gemini_response = self.process_gemini_response(response.text)

            # Eliminar los primeros dos elementos de subtemas de cada tema (son irrelevantes, generan asteriscos)
            filtered_response = []
            for tema in gemini_response: # Esto se puede mejorar
                tema["subtemas"] = tema["subtemas"][2:]  # Eliminar los primeros dos elementos
                if tema["subtemas"]:  # Si hay subtemas después del corte
                    filtered_response.append(tema)  # Agregar el tema solo si tiene subtemas



            return Response({
                "temas": filtered_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred: {e}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def extract_relevant_content(self, doc):
        """
        Extrae el contenido a partir de la sección que comienza con "APRENDIZAJES Y CONTENIDOS"
        """
        content = []
        started = False

        # Recorrer todos los párrafos del documento
        for para in doc.paragraphs:
            para_text = para.text.strip()

            if not started:
                # Buscar la palabra clave "APRENDIZAJES Y CONTENIDOS"
                if "APRENDIZAJES Y CONTENIDOS" in para_text:
                    started = True  # Comienza a extraer después de encontrar la sección
            if started:
                # Agregar los párrafos después de encontrar la sección
                content.append(para_text)

        return '\n'.join(content)  # Devolver el contenido relevante como un solo string

    def process_gemini_response(self, gemini_text):
        """
        Procesar la respuesta de la API de Gemini para estructurarla en temas y subtemas.
        """
        temas = []
        tema_actual = None
        subtemas_actuales = []

        lines = gemini_text.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith("**") and line.endswith("**"):  # Identificar temas principales (Ej: "**Tema 1**")
                if tema_actual:
                    temas.append({
                        "tema": tema_actual,
                        "subtemas": subtemas_actuales
                    })
                tema_actual = line[2:-2]  # Extraer el nombre del tema (eliminando los asteriscos)
                subtemas_actuales = []  # Reiniciar subtemas
            elif line.startswith("*"):  # Identificar subtemas (Ej: "* Subtema 1")
                subtemas_actuales.append(line[2:])  # Extraer el subtema (eliminando el asterisco y espacio)

        # Agregar el último tema al final
        if tema_actual:
            temas.append({
                "tema": tema_actual,
                "subtemas": subtemas_actuales
            })

        return temas

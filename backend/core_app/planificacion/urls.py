from django.urls import path
from .views import PDFExtractTextView, RegisterPlanificacionView, ListPlanificacionView, WordFileProcessor

urlpatterns = [
    path('register/', RegisterPlanificacionView.as_view(), name='register_planificacion'),
    path('list/', ListPlanificacionView.as_view(), name='list_planificacion'),
    path('process_word/', WordFileProcessor.as_view(), name='process_word'),
    path('extract-pdf-text/', PDFExtractTextView.as_view(), name='extract_pdf_text'),
]
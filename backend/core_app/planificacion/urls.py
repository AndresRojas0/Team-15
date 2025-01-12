from django.urls import path
from .views import PDFExtractTextView, RegisterPlanificacionView, ListPlanificacionView, WordFileProcessor, UpdatePlanificacionView, DeletePlanificacionView

urlpatterns = [
    path('register/', RegisterPlanificacionView.as_view(), name='register_planificacion'),
    path('list/', ListPlanificacionView.as_view(), name='list_planificacion'),
    path('process_word/', WordFileProcessor.as_view(), name='process_word'),
    path('extract-pdf-text/', PDFExtractTextView.as_view(), name='extract_pdf_text'),
    path('update/<int:pk>/', UpdatePlanificacionView.as_view(), name='update_planificacion'),
    path('delete/<int:pk>/', DeletePlanificacionView.as_view(), name='delete_planificacion'),
]
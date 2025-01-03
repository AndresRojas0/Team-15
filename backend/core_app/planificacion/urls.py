from django.urls import path
from .views import RegisterPlanificacionView, ListPlanificacionView, WordFileProcessor

urlpatterns = [
    path('register/', RegisterPlanificacionView.as_view(), name='register_planificacion'),
    path('list/', ListPlanificacionView.as_view(), name='list_planificacion'),
    path('process_word/', WordFileProcessor.as_view(), name='process_word'),
]
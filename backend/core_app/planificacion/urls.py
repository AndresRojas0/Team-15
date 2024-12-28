from django.urls import path
from .views import ProcessPlanificacionExcelView, RegisterPlanificacionView, ListPlanificacionView

urlpatterns = [
    path('register/', RegisterPlanificacionView.as_view(), name='register_planificacion'),
    path('list/', ListPlanificacionView.as_view(), name='list_planificacion'),
    path('process_excel/', ProcessPlanificacionExcelView.as_view(), name='process_planificacion_excel'),
]
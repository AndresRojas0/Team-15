from django.urls import path
from planificacion_mensual.views import ListPlanificacionMensualView, PlanificacionMensualView, PlanificacionMensualBulkView

urlpatterns = [
    path('register/', PlanificacionMensualView.as_view(), name='register_planificacion_mensual'),
    path('list-register/', PlanificacionMensualBulkView.as_view(), name='list_register_planificacion_mensual'),
    path('list/', ListPlanificacionMensualView.as_view(), name='list_planificacion_mensual'),
]

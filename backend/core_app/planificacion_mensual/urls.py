from django.urls import path
from planificacion_mensual.views import ListPlanificacionMensualView, PlanificacionMensualView, PlanificacionMensualBulkView, UpdatePlanificacionMensualView, DeletePlanificacionMensualView

urlpatterns = [
    path('register/', PlanificacionMensualView.as_view(), name='register_planificacion_mensual'),
    path('list-register/', PlanificacionMensualBulkView.as_view(), name='list_register_planificacion_mensual'),
    path('list/', ListPlanificacionMensualView.as_view(), name='list_planificacion_mensual'),
    path('update/<int:pk>/', UpdatePlanificacionMensualView.as_view(), name='update_planificacion_mensual'),
    path('delete/<int:pk>/', DeletePlanificacionMensualView.as_view(), name='delete_planificacion_mensual'),

]

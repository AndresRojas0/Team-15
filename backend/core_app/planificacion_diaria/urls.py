from django.urls import path
from .views import RegisterPlanificacionDiariaViewSet, ListPlanificacionDiariaViewSet, UpdatePlanificacionDiaria, DeletePlanificacionDiaria

urlpatterns = [
    path('register/', RegisterPlanificacionDiariaViewSet.as_view({'post': 'create'}), name='register_planificacion_diaria'),
    path('list/', ListPlanificacionDiariaViewSet.as_view({'get': 'list'}), name='list_planificacion_diaria'),
    path('update/<int:pk>/', UpdatePlanificacionDiaria.as_view({'put': 'partial_update'}), name='update_planificacion_diaria'),
    path('delete/<int:pk>/', DeletePlanificacionDiaria.as_view({'delete': 'destroy'}), name='delete_planificacion_diaria')
]
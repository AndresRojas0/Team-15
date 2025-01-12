from django.urls import path
from examen_asignado.views import RegisterExamenAsignadoViewSet, ListExamenAsignadoViewSet, UpdateExamenAsignadoViewSet, DeleteExamenAsignadoViewSet

urlpatterns = [
    path('register/', RegisterExamenAsignadoViewSet.as_view({'post': 'create'}), name='register_examen_asignado'),
    path('list/', ListExamenAsignadoViewSet.as_view({'get': 'list'}), name='list_examen_asignado'),
    path('update/<int:pk>/', UpdateExamenAsignadoViewSet.as_view({'put': 'partial_update'}), name='update_examen_asignado'),
    path('delete/<int:pk>/', DeleteExamenAsignadoViewSet.as_view({'delete': 'destroy'}), name='delete_examen_asignado'),
]
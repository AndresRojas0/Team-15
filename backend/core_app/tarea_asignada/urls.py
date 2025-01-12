from django.urls import path
from tarea_asignada.views import RegisterTareaAsignadaViewSet, ListTareaAsignadaViewSet, UpdateTareaAsignadaViewSet, DeleteTareaAsignadaViewSet

urlpatterns = [
    path('register/', RegisterTareaAsignadaViewSet.as_view({'post': 'create'}), name='register_tarea_asignada'),
    path('list/', ListTareaAsignadaViewSet.as_view({'get': 'list'}), name='list_tarea_asignada'),
    path('update/<int:pk>/', UpdateTareaAsignadaViewSet.as_view({'put': 'partial_update'}), name='update_tarea_asignada'),
    path('delete/<int:pk>/', DeleteTareaAsignadaViewSet.as_view({'delete': 'destroy'}), name='delete_tarea_asignada'),
]
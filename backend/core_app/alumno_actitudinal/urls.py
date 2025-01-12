from django.urls import path
from .views import RegisterAlumnoActitudinal, ListAlumnoActitudinal, UpdateAlumnoActitudinal, DeleteAlumnoActitudinal


urlpatterns = [
    path('register/', RegisterAlumnoActitudinal.as_view(), name='alumno_actitudinal_register'),
    path('list/', ListAlumnoActitudinal.as_view(), name='list_alumno_actitudinal'),
    path('update/<int:pk>/', UpdateAlumnoActitudinal.as_view({'put': 'partial_update'}), name='update_alumno_actitudinal'),
    path('delete/<int:pk>/', DeleteAlumnoActitudinal.as_view(), name='delete_alumno_actitudinal'),
]
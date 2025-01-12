from django.urls import path
from .views import RegisterAlumnoAsistencia, ListAlumnoAsistencia, UpdateAlumnoAsistencia, DeleteAlumnoAsistencia


urlpatterns = [
    path('register/', RegisterAlumnoAsistencia.as_view(), name='alumno_asistencia_register'),
    path('list/', ListAlumnoAsistencia.as_view(), name='alumno_asistencia_list'),
    path('update/<int:pk>/', UpdateAlumnoAsistencia.as_view({'put': 'partial_update'}), name='update_alumno_asistencia'),
    path('delete/<int:pk>/', DeleteAlumnoAsistencia.as_view(), name='delete_alumno_asistencia'),
]
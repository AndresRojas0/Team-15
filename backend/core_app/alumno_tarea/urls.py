from django.urls import path
from alumno_tarea.views import RegisterAlumnoTarea, ListAlumnoTarea, UpdateAlumnoTarea, DeleteAlumnoTarea

urlpatterns = [
    path('register/', RegisterAlumnoTarea.as_view(), name='register_alumno_tarea'),
    path('list/', ListAlumnoTarea.as_view(), name='list_alumno_tarea'),
    path('update/<int:pk>/', UpdateAlumnoTarea.as_view(), name='update_alumno_tarea'),
    path('delete/<int:pk>/', DeleteAlumnoTarea.as_view(), name='delete_alumno_tarea'),
]
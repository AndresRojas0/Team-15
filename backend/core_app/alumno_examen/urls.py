from django.urls import path
from .views import RegisterAlumnoExamenView, ListAlumnoExamenView, UpdateAlumnoExamenView, DeleteAlumnoExamenView

urlpatterns = [
    path('register/', RegisterAlumnoExamenView.as_view(), name='alumno_examen_register'),
    path('list/', ListAlumnoExamenView.as_view(), name='alumno_examen_list'),
    path('update/<int:pk>/', UpdateAlumnoExamenView.as_view(), name='alumno_examen_update'),
    path('delete/<int:pk>/', DeleteAlumnoExamenView.as_view(), name='alumno_examen_delete')
]
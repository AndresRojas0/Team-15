from django.urls import path
from .views import DeleteAlumnoView, ProcessAlumnoExcelView, RegisterAlumnoView, RegisterAlumnosView, ListAlumnoView, UpdateAlumnoView

urlpatterns = [
    path('list-register/', RegisterAlumnosView.as_view(), name='register_alumno'),
    path('list/', ListAlumnoView.as_view(), name='list_alumno'),
    path('process_excel/', ProcessAlumnoExcelView.as_view(), name='process_alumno_excel'),
    path('register/', RegisterAlumnoView.as_view(), name='register_alumno'),
    path('update/<int:pk>/', UpdateAlumnoView.as_view(), name='update_alumno'),
    path('delete/<int:pk>/', DeleteAlumnoView.as_view(), name='delete_alumno'),
]
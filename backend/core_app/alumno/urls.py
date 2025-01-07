from django.urls import path
from .views import ProcessAlumnoExcelView, RegisterAlumnoView, RegisterAlumnosView, ListAlumnoView

urlpatterns = [
    path('list-register/', RegisterAlumnosView.as_view(), name='register_alumno'),
    path('list/', ListAlumnoView.as_view(), name='list_alumno'),
    path('process_excel/', ProcessAlumnoExcelView.as_view(), name='process_alumno_excel'),
    path('register/', RegisterAlumnoView.as_view(), name='register_alumno'),
    
]
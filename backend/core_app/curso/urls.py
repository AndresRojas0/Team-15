from django.urls import path
from .views import DeleteCursoView, ListCursoView, RegisterCursoView, UpdateCursoView

urlpatterns = [
    path('register/', RegisterCursoView.as_view(), name='register_curso'),
    path('update/', UpdateCursoView.as_view(), name='update_curso'),
    path('list/', ListCursoView.as_view(), name='list_curso'),
    path('delete/<int:pk>/', DeleteCursoView.as_view(), name='delete_curso'),
]
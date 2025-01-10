from django.urls import path
from .views import ListRecursoView, RegisterRecursoView

urlpatterns = [
    path('register/', RegisterRecursoView.as_view(), name='register_recurso'),
    path('list/', ListRecursoView.as_view(), name='list_recurso'),
]
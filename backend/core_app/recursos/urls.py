from django.urls import path
from .views import RegistrarRecursoViewSet, ListRecursosViewSet


urlpatterns = [
    path('register/', RegistrarRecursoViewSet.as_view({'post': 'post'}), name='subir-recurso'),
    path('list/', ListRecursosViewSet.as_view({'get': 'list'}), name='listar-recursos')
]
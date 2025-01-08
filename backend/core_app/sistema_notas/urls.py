from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListSistemaNotasViewSet, SistemaNotasViewSet

router = DefaultRouter()
router.register(r'register', SistemaNotasViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('curso/<int:curso_id>/', ListSistemaNotasViewSet.as_view(), name='list-sistema-notas-por-curso'),
    path('list/', ListSistemaNotasViewSet.as_view(), name='list-sistema-notas-por-curso'),
]
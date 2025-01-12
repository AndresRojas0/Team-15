from django.urls import path

from .views import TemaViewSet, RegisterViewSet, UpdateViewSet, DeleteViewSet


urlpatterns = [
    path('all/', TemaViewSet.as_view({'get': 'list'})),
    path('register/', RegisterViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/', UpdateViewSet.as_view({'put': 'partial_update'})),
    path('delete/<int:pk>/', DeleteViewSet.as_view({'delete': 'destroy'})),
]
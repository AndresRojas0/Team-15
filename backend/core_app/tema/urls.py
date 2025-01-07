from django.urls import path

from .views import TemaViewSet, RegisterViewSet


urlpatterns = [
    path('all/', TemaViewSet.as_view({'get': 'list'})),
    path('register/', RegisterViewSet.as_view({'post': 'create'})),
]
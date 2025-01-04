from django.urls import path

from .views import TemaViewSet


urlpatterns = [
    path('all/', TemaViewSet.as_view({'get': 'list'})),
]
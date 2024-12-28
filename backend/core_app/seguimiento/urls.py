from django.urls import path
from .views import RegisterSeguimientoView, ListSeguimientoView

urlpatterns = [
    path('register/', RegisterSeguimientoView.as_view(), name='register_seguimiento'),
    path('list/', ListSeguimientoView.as_view(), name='list_seguimiento'),
]
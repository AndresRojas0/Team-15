from django.urls import path
from .views import RegisterPlanificacionView, ListPlanificacionView

urlpatterns = [
    path('register/', RegisterPlanificacionView.as_view(), name='register_planificacion'),
    path('list/', ListPlanificacionView.as_view(), name='list_planificacion'),
]
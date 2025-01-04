from django.urls import path
from .views import ListAllSubtemasView

urlpatterns = [
    path('all/', ListAllSubtemasView.as_view(), name='list-all-subtemas'),
]
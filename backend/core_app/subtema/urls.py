from django.urls import path
from .views import ListAllSubtemasView, RegisterSubtemaView

urlpatterns = [
    path('all/', ListAllSubtemasView.as_view(), name='list-all-subtemas'),
    path('register/', RegisterSubtemaView.as_view(), name='create'),
]
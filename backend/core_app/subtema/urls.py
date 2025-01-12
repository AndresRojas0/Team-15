from django.urls import path
from .views import ListAllSubtemasView, RegisterSubtemaView, UpdateSubtemaView, DeleteSubtemaView

urlpatterns = [
    path('all/', ListAllSubtemasView.as_view(), name='list-all-subtemas'),
    path('register/', RegisterSubtemaView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateSubtemaView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteSubtemaView.as_view(), name='delete'),
]
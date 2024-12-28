from django.urls import path
from .views import ListMateriaView, RegisterMateriaView

urlpatterns = [
    path('register/', RegisterMateriaView.as_view(), name='register_materia'),
    path('list/', ListMateriaView.as_view(), name='list_materia'),
]
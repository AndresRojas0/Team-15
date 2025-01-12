from django.urls import path
from .views import ListMateriaView, RegisterMateriaView, UpdateMateriaView, DeleteMateriaView

urlpatterns = [
    path('register/', RegisterMateriaView.as_view(), name='register_materia'),
    path('list/', ListMateriaView.as_view(), name='list_materia'),
    path('update/<int:pk>/', UpdateMateriaView.as_view(), name='update_materia'),
    path('delete/<int:pk>/', DeleteMateriaView.as_view(), name='delete_materia')
]
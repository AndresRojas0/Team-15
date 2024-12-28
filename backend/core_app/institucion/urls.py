from django.urls import path
from .views import DeleteInstitucionView, ListInstitucionView, RegisterInstitucionView, UpdateInstitucionView

urlpatterns = [
    path('register/', RegisterInstitucionView.as_view(), name='register_institucion'),
    path('list/', ListInstitucionView.as_view(), name='list_institucion'),
    path('update/', UpdateInstitucionView.as_view(), name='update_institucion'),
    path('delete/<int:pk>/', DeleteInstitucionView.as_view(), name='delete_institucion'),
]
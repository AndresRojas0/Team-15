from django.urls import path
from .views import RecursoURLView

urlpatterns = [
    path('upload-file/', RecursoURLView.as_view(), name='upload-file')
]
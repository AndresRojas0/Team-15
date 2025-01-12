from django.urls import path
from .views import DeleteSubtemaAnualView, SubtemaAnualViewSet, ListSubtemaAnualView, BulkCreateSubtemaAnualView, UpdateSubtemaAnualView

urlpatterns = [
    path('register/', SubtemaAnualViewSet.as_view({'post': 'create'})),
    path('list/', ListSubtemaAnualView.as_view(), name='list-subtemas-anuales'),
    path('list-register/', BulkCreateSubtemaAnualView.as_view(), name='bulk-create-subtemas-anuales'),
    path('update/<int:pk>/', UpdateSubtemaAnualView.as_view(), name='update-subtema-anual'),
    path('delete/<int:pk>/', DeleteSubtemaAnualView.as_view(), name='delete-subtema-anual'),
]
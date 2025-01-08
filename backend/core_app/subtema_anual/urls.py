from django.urls import path
from .views import SubtemaAnualViewSet, ListSubtemaAnualView, BulkCreateSubtemaAnualView

urlpatterns = [
    path('register/', SubtemaAnualViewSet.as_view({'post': 'create'})),
    path('update/<int:pk>/', SubtemaAnualViewSet.as_view({'put': 'update'})),
    path('list/', ListSubtemaAnualView.as_view(), name='list-subtemas-anuales'),
    path('list-register/', BulkCreateSubtemaAnualView.as_view(), name='bulk-create-subtemas-anuales'),
]
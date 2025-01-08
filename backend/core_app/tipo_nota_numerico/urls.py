from django.urls import path, include
from tipo_nota_numerico.views import ListTipoNotaNumericaAuth


urlpatterns = [
    path('all/', ListTipoNotaNumericaAuth.as_view({'get': 'list'})),
]

from django.urls import path
from autenticacion.views import BasicLoginView, DeleteUserView, GoogleOAuthService, RegisterUserView, TokenDataView, TokenRefreshView, UpdateUserView

urlpatterns = [
    path('google-login/', GoogleOAuthService.as_view(), name='google-oauth'),
    path('basic-login/', BasicLoginView.as_view(), name='basic-login'),
    path('basic-register/', RegisterUserView.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name='update-user'),
    path('delete/', DeleteUserView.as_view(), name='delete-user'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token-data/', TokenDataView.as_view(), name='token-data'),
]
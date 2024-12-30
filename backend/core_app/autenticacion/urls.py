from django.urls import path
from autenticacion.views import BasicLoginView, DeleteUserView, GoogleOAuthService, RecoverPasswordView, RegisterUserView, PasswordResetView, TokenDataView, TokenRefreshView, UpdateUserView, VerifyEmailView

urlpatterns = [
    path('google-login/', GoogleOAuthService.as_view(), name='google-oauth'),
    path('basic-login/', BasicLoginView.as_view(), name='basic-login'),
    path('basic-register/', RegisterUserView.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name='update-user'),
    path('delete/', DeleteUserView.as_view(), name='delete-user'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token-data/', TokenDataView.as_view(), name='token-data'),

    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('recover-password/', RecoverPasswordView.as_view(), name='recover-password'),
    path('reset-password/<str:token>/', PasswordResetView.as_view(), name='reset-password'),

]
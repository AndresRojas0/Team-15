import secrets
import string
from django.shortcuts import get_object_or_404
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from autenticacion.models import CustomUser
from autenticacion.permissions import IsAdminUser
from .serializer import CustomUserSerializer, PasswordResetSerializer
from rest_framework import generics
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings

class GoogleOAuthService(APIView):
    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH_CLIENT_SECRET
    redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

    def post(self, request):
        authorization_code = request.data.get("code")
        token = self.exchange_authorization_code_for_token(authorization_code)
        if token:
            user_profile = self.get_user_profile(token)
            email = user_profile.get("email")
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                except CustomUser.DoesNotExist:
                    # Generar una contraseña aleatoria
                    alphabet = string.ascii_letters + string.digits
                    random_password = ''.join(secrets.choice(alphabet) for i in range(12))
                    
                    # Crear el usuario sin el username para obtener el id
                    user = CustomUser(
                        first_name=user_profile.get("given_name", ""),
                        last_name=user_profile.get("family_name", ""),
                        email=email,
                        role='user'
                    )
                    user.set_password(random_password)  # Establecer la contraseña aleatoria
                    user.save()

                    # Generar un nombre de usuario único con el id
                    user.username = f"{user.first_name}{user.last_name}_{user.id}"
                    user.save()

                refresh = RefreshToken.for_user(user)
                user_data = CustomUserSerializer(user).data
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_data
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No email found in user profile"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Error al obtener el access token"}, status=status.HTTP_400_BAD_REQUEST)

    def exchange_authorization_code_for_token(self, authorization_code):
        token_request_data = {
            "code": authorization_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post("https://oauth2.googleapis.com/token", data=token_request_data)
        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("access_token")
        else:
            return None

    def get_user_profile(self, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Error al obtener el perfil del usuario"}



class BasicLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(password):
            if not user.email_verified:
                return Response({"error": "Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)

            token = user.get_token()
            user_data = CustomUserSerializer(user).data

            return Response({
                'refresh_token': str(token),
                'access_token': str(token.access_token),
                'user': user_data
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

from django.core.mail import EmailMessage

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = user.get_token()
        user_data = CustomUserSerializer(user).data

        # Crear el enlace de verificación
        verification_url = request.build_absolute_uri(
            reverse('verify-email', kwargs={'token': user.email_verification_token})
        )

        # Crear el contenido HTML del correo
        html_content = f"""
        <html>
        <body>
            <h1>¡Bienvenido a PalProfe!</h1>
            <p>Gracias por registrarte. Por favor, hace clic en el siguiente enlace para confirmar tu correo electrónico:</p>
            <a href="{verification_url}">Confirmar correo electrónico</a>
            <br><br>
            <img src="{settings.PALPROFE_ICON_URL}" alt="PalProfe icon" width="300" height="250">
        </body>
        </html>
        """

        # Enviar el correo de verificación
        email = EmailMessage(
            'Confirma tu correo electrónico',
            html_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = 'html'  # Definir el contenido como HTML
        email.send()

        return Response({
            'message': 'Se ha enviado un correo de verificación a su dirección de correo electrónico. Por favor, verifique su correo para completar el registro.'
        }, status=status.HTTP_201_CREATED)
    
    
    
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return Response({'error': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid authorization header format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access = AccessToken(token)
            user_id = access['user_id']
        except TokenError:
            return Response({'error': 'Token is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # instance obtiene el usuario a actualizar
        if isinstance(instance, Response):
            return instance  # Si get_object devuelve una respuesta de error, la retornamos directamente
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # partial=True permite actualizaciones parciales
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = CustomUserSerializer(user).data

        return Response({
            'user': user_data
        }, status=status.HTTP_200_OK)
    

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_object(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return Response({'error': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid authorization header format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access = AccessToken(token)
            user_id = access['user_id']
        except TokenError:
            return Response({'error': 'Token is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return user

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # instance obtiene el usuario a eliminar
        if isinstance(instance, Response):
            return instance  # Si get_object devuelve una respuesta de error, la retornamos directamente
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TokenRefreshView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh_token')
        if not refresh:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh)
            user = CustomUser.objects.get(id=refresh['user_id'])
        except TokenError:
            return Response({'error': 'Refresh token is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({'error': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        

class TokenDataView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # El token debe estar en el formato "Bearer <token>"
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return Response({'error': 'Invalid token type'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid authorization header format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Intenta usar el token como un token de acceso
            access = AccessToken(token)
            user_id = access['user_id']
            role = access['role']
        except TokenError:
            try:
                # Si falla, intenta usar el token como un token de refresco
                refresh = RefreshToken(token)
                user_id = refresh['user_id']
                role = refresh['role']
            except TokenError:
                return Response({'error': 'Token is expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({'error': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'user_id': user_id, 'role': role}, status=status.HTTP_200_OK)
    

class VerifyEmailView(APIView):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, email_verification_token=token)
        user.email_verified = True
        user.email_verification_token = None
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    

class RecoverPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = get_object_or_404(CustomUser, email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Generar un nuevo token de recuperación de contraseña
            alphabet = string.ascii_letters + string.digits
            recovery_token = ''.join(secrets.choice(alphabet) for i in range(32))
            user.recovery_token = recovery_token
            user.save()
            
            # Crear el enlace de recuperación de contraseña
            recovery_url = request.build_absolute_uri(
                reverse('reset-password', kwargs={'token': recovery_token})
            )
            
            # Crear el contenido HTML del correo
            html_content = f"""
            <html>
            <body>
                <h1>Recuperación de contraseña</h1>
                <p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
                <a href="{recovery_url}">Restablecer contraseña</a>
            </body>
            </html>
            """
            
            # Enviar el correo de recuperación de contraseña
            email = EmailMessage(
                'Recuperación de contraseña',
                html_content,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.content_subtype = 'html'  # Definir el contenido como HTML
            email.send()
            
            return Response({'message': 'Password recovery email sent'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'An error occurred while processing your request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class PasswordResetView(APIView):
    def post(self, request, token):
        try:
            user = CustomUser.objects.get(recovery_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.recovery_token = None
            user.save()
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

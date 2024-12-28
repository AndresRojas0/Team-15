import secrets
import string
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from autenticacion.models import CustomUser
from autenticacion.permissions import IsAdminUser
from .serializer import CustomUserSerializer
from rest_framework import generics
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

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
            token = user.get_token()
            user_data = CustomUserSerializer(user).data
            return Response({
                'refresh_token': str(token),
                'access_token': str(token.access_token),
                'user': user_data
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = user.get_token()
        user_data = CustomUserSerializer(user).data

        return Response({
            'refresh_token': str(token),
            'access_token': str(token.access_token),
            'user': user_data
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
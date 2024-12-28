from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from .models import Institucion
from .serializer import InstitucionSerializer
from django.db import IntegrityError

class RegisterInstitucionView(generics.CreateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
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
        
        data = request.data.copy()
        data['docente'] = user_id  # Asigna el docente_id al user_id extraído del token
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
            institucion = serializer.save()
        except IntegrityError:
            return Response({'error': 'Institution with this name already exists for this user'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'institucion': InstitucionSerializer(institucion).data
        }, status=status.HTTP_201_CREATED)


class ListInstitucionView(generics.ListAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Institucion.objects.filter(docente=self.request.user)
        return queryset
    

class UpdateInstitucionView(generics.UpdateAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
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
        
        institucion_id = request.data.get('id')
        if not institucion_id:
            return Response({'error': 'Institution ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            instance = Institucion.objects.get(id=institucion_id, docente_id=user_id)
        except Institucion.DoesNotExist:
            return Response({'error': 'Institution not found or you do not have permission to update this institution'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'institucion': InstitucionSerializer(instance).data
        }, status=status.HTTP_200_OK)
    

class DeleteInstitucionView(generics.DestroyAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
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
        
        institucion_id = kwargs.get('pk')
        if not institucion_id:
            return Response({'error': 'Institution ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            instance = Institucion.objects.get(id=institucion_id, docente_id=user_id)
        except Institucion.DoesNotExist:
            return Response({'error': 'Institution not found or you do not have permission to delete this institution'}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
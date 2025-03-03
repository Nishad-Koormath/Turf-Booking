from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404 
from .models import CustomUser


# Create your views here.

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    def post(self, request):
          try:
              refresh_token = request.data["refresh"]
              token = RefreshToken(refresh_token)
              token.blacklist()
              return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
          except Exception as e:
              return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
          
class GetUserByIdView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


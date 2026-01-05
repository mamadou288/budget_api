from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView


class RegisterView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

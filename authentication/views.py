from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
        except ValueError as e:
            if str(e) == "EMAIL_TAKEN":
                return Response(
                    {"detail": "Email déjà utilisé."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if str(e) == "USERNAME_TAKEN":
                return Response(
                    {"detail": "Username déjà utilisé."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            raise

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .services import authenticate_by_email, create_user_account


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate_by_email(email=email, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Identifiants invalides."})

        refresh = self.get_token(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=30)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    def create(self, validated_data):
        return create_user_account(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email et mot de passe requis.")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError("Identifiants invalides.")

        return super().validate({"username": user.username, "password": password})


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        # create_user hash le password correctement
        return User.objects.create_user(
            username=validated_data["email"],  # utile même si tu n’exposes pas username
            email=validated_data["email"],
            password=validated_data["password"],
        )

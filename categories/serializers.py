from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "type", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

        def create(self, validated_data):
            request = self.context["request"]
            return Category.objects.create(user=request.user, **validated_data)

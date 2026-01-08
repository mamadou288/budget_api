from rest_framework import serializers
from .models import Transaction
from categories.models import Category


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "type",
            "amount",
            "occurred_at",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_category(self, category: Category) -> Category:
        request = self.context.get("request")
        if request and category.user_id != request.user.id:
            raise serializers.ValidationError("This category does not belong to the current user.")
        return category

    def validate(self, attrs):
        """
        Règle: transaction.type doit matcher category.type.
        Gère aussi le PATCH (si category ou type n'est pas fourni).
        """
        category = attrs.get("category") or getattr(self.instance, "category", None)
        tx_type = attrs.get("type") or getattr(self.instance, "type", None)

        if category and tx_type and category.type != tx_type:
            raise serializers.ValidationError({"type": "Transaction type must match category type."})

        return attrs

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "description", "amount", "type", "timestamp"]

    def validate_amount(self, value):
        if(value <= 0):
            raise serializers.ValidationError("Amount must be positive.")
        return value
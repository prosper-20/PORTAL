from rest_framework import serializers
from accounts.models import CustomUser


def validate_email(self, value):
        try:
            user = CustomUser.objects.get(user=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Email address is wrong")
        return user
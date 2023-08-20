from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =["user", "first_name", "last_name", "is_employer"]






class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password":{"write_only": True}
        }

    
    def save(self):
        user = CustomUser(
            email = self.validated_data["email"],
            username = self.validated_data["username"]
        )
       

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Response": "Both passwords must match"})
        user.set_password(make_password(password))
        user.save()
        return user
    


class EmployerRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password":{"write_only": True}
        }

    
    def save(self):
        user = CustomUser(
            email = self.validated_data["email"],
            username = self.validated_data["username"]
        )
       

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Response": "Both passwords must match"})
        user.set_password(password)
        user.profile.is_employer = True
        user.save()
        return user



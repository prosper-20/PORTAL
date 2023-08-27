from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Profile
        fields =["user", "first_name", "last_name", "is_employer"]


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        print(data)
        user = authenticate(**data)
        print(user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError()






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



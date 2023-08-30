from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.hashers import make_password
from .validators import validate_email
from django.contrib.auth import authenticate

class AdminCustomUserSerializer(serializers.ModelSerializer):
    no_of_users = serializers.SerializerMethodField("get_number_of_users")
    
    class Meta:
        model = CustomUser
        fields = ["no_of_users"]

    def get_number_of_users(cls, *args):
        return CustomUser.objects.all().count()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Profile
        fields =["user", "first_name", "last_name", "avatar", "cv", "bio", "country", "phone_number"]


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
    supporting_documents = serializers.FileField(max_length=None, allow_empty_file=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2", "supporting_documents"]
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
        # user.profile.is_employer = True
        user.save()
        return user
    


class EmailExistsValidator:
    def __init__(self, queryset=CustomUser.objects.all(), message="This email address does not exist."):
        self.queryset = queryset
        self.message = message

    def __call__(self, value):
        if not self.queryset.filter(email=value).exists():
            raise serializers.ValidationError(self.message)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailExistsValidator()])


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)


#     def validate_email(self, value):
#         user = CustomUser.objects.get(email=value)
#         print(user)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Email not found")



    




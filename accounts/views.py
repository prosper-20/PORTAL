from django.shortcuts import render
from .serializers import (UserRegistrationSerializer, 
                          EmployerRegistrationSerializer,
                          CustomUserSerializer,
                          UserLoginSerializer,
                          ProfileSerializer,
                          AdminCustomUserSerializer,
                          PasswordResetSerializer,
                          ChangePasswordSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, Profile
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = CustomUser.objects.get(email=request.user)
        print(user)
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data["new_password"]
        confirm_new_password = serializer.data["confirm_new_password"]

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Both passwords must match!")
        user.set_password(confirm_new_password)
        user.save()
        message = {"Success": "Password reset successful!",
                   "Click to login": "http://127.0.0.1:8000/accounts/signin/"}
        return Response(message, status=status.HTTP_202_ACCEPTED)
    
        


class PasswordResetView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = "Password Reset !!"
        message = render_to_string('password_reset.html', {
            'domain': 'http://127.0.0.1:8000/accounts/me/password-change/'
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        current_email = serializer.data["email"]
        to_email = [current_email]
        # send_mail(subject, message, from_email, to_email)
        msg = EmailMessage(subject, message, from_email, to_email)
        msg.content_subtype = 'html'
        msg.send()

        return Response("Password Reset Email Sent!", status=status.HTTP_200_OK)

class AllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        all_users = CustomUser.objects.all()
        serialized_users = AdminCustomUserSerializer(all_users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)

class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "Account creation successful"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)

class EmployerSignUp(APIView):
    def post(self, request, format=None):
        serializer = EmployerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "Your account is currently undergoing validation, your employer status will be updated in 24 hours. Thank you!"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)

class MyAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "User details updated successfully"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_200_OK)
    

    def delete(self, request, format=None):
        current_user = CustomUser.objects.filter(email=request.user)
        current_user.delete()
        message = {"Success", "Account deletion successful"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "Your account has been updated successfully!!"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_202_ACCEPTED)
    

        


    

    

    

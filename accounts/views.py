from django.shortcuts import render
from .serializers import (UserRegistrationSerializer, 
                          EmployerRegistrationSerializer,
                          CustomUserSerializer,
                          UserLoginSerializer,
                          ProfileSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView

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
        message = {"Success": "You have been successfully created as an employer"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)

class MyAccountView(LoginRequiredMixin, APIView):
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
    

    

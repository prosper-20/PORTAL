from django.shortcuts import render
from .serializers import (UserRegistrationSerializer, 
                          EmployerRegistrationSerializer,
                          CustomUserSerializer,
                          ProfileSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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

class MyAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

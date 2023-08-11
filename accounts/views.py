from django.shortcuts import render
from .serializers import UserRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "Account creation successful"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)

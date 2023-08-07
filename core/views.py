from django.shortcuts import render
from .serializers import JobSerializer, ApplicationSerialzier
from .models import Job, Application
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ApplicationHomePage(APIView):
    def get(self, request, format=None, **kwargs):
        job = Job.objects.get(id=kwargs.get("id"))
        applications = Application.objects.filter(job=job)
        serializer = ApplicationSerialzier(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class JobHomePage(APIView):
    def get(self, request, format=None):
        serializer_context = {
            'request': request,
        }
        all_jobs = Job.objects.all()
        serializer = JobSerializer(all_jobs, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class JobDetailPage(APIView):
    def get(self, request, format=None, **kwargs):
        slug = kwargs.get("slug")
        id = kwargs.get("id")
        
        try:
            if id:
                job = Job.objects.get(id=id)
            elif slug:
                job = Job.objects.get(slug=slug)
            elif job and slug:
                job = Job.objects.get(id=id, slug=slug)
        except Job.DoesNotExist:
                return Response("Job not found", status=status.HTTP_404_NOT_FOUND)
        serializer_context = {
            'request': request,
        }
        
        serializer = JobSerializer(job, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
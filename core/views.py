from django.shortcuts import render
from .serializers import JobSerializer, ApplicationsSerialzier
from .models import Job, Application
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ApplicationHomePage(APIView):
    def get(self, request, format=None, **kwargs):
        job = Job.objects.get(id=kwargs.get("id"))
        applications = Application.objects.filter(job=job)
        serializer = ApplicationsSerialzier(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, format=None, **kwargs):
        job_id = kwargs.get('job_id')  # Assuming 'job_id' is a parameter in the URL
        job = Job.objects.get(id=job_id)
        current_job = Application(job=job)
        serializer = ApplicationsSerialzier(current_job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"Success": "Application has been submitted"}
        message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)
    
    # def perform_create(self, serializer):
        
    #     job_id = self.kwargs.get("id")
    #     print(job_id)
    #     job = Job.objects.get(id=job_id)
    #     serializer.save(job=job)


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
            
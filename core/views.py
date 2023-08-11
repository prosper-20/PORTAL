from django.shortcuts import render
from .serializers import JobSerializer, ApplicationsSerialzier
from .models import Job, Application
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .permissions import CompleteProfilePermission, CanViewJobApplications
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions


class ApplicationHomePage(ListCreateAPIView):
    
    serializer_class = ApplicationsSerialzier
    permission_classes = [IsAuthenticated, CanViewJobApplications]

    def get_queryset(self):
        id = self.kwargs.get("id")
        return Application.objects.filter(job=id)



# class ApplicationHomePage(APIView):
#     # permission_classes = [IsAuthenticated, CanViewJobApplications]
#     def get_permissions(self):
#         return (permissions.IsAuthenticated(), CanViewJobApplications())

#     # def post_permissions(self):
#     #     return [IsAuthenticated, CompleteProfilePermission()]
    

#     def get(self, request, format=None, **kwargs):
#         job = Job.objects.get(id=kwargs.get("id"))
#         applications = Application.objects.filter(job=job)
#         serializer = ApplicationsSerialzier(applications, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

#     def post(self, request, format=None, **kwargs):
#         job_id = kwargs.get('id')  # Assuming 'job_id' is a parameter in the URL
#         job = Job.objects.get(id=job_id)
#         if request.user.is_authenticated:
#             user = CustomUser.objects.get(email=request.user)
#             print(request.user)
#             current_job = Application.objects.create(job=job, first_name=user.profile.first_name, last_name=user.profile.last_name, email=user.email, cv=user.profile.cv, country=user.profile.country)
#             serializer = ApplicationsSerialzier(current_job)
#             message = {"Success": "Application has been submitted"}
#             message.update(serializer.data)
#         else:
#             current_job = Application(job=job)
#             serializer = ApplicationsSerialzier(current_job, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             message = {"Success": "Application has been submitted"}
#             message.update(serializer.data)
#         return Response(message, status=status.HTTP_201_CREATED)
    
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
            
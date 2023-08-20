from django.shortcuts import render, get_object_or_404
from .serializers import JobSerializer, ApplicationsSerialzier
from .models import Job, Application
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import CompleteProfilePermission, CanViewJobApplications
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import HasCompleteProfile

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


# class JobHomePage(APIView):
    
#     def get(self, request, format=None):
#         serializer_context = {
#             'request': request,
#         }
#         all_jobs = Job.objects.all()
#         serializer = JobSerializer(all_jobs, many=True, context=serializer_context)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request, format=None):
#         if not request.user.is_authenticated:
#             return Response({"Message": "Login to create a job posting"}, status=status.HTTP_401_UNAUTHORIZED)
#         elif request.user.profile.is_employer == False:
#             return Response({"Message": "Only users who are employers can post jobs"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         new_job = JobSerializer(data=request.data)
#         new_job.is_valid(raise_exception=True)
        
#         message = {"Success": "Job has been created successfully!!"}
#         message.update(new_job.data)
#         return Response(message, status=status.HTTP_201_CREATED)


class JobHomePage(ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    search_fields = ["company_name", "title", "location"]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['company_name', 'expired']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # Specify your desired permission class for GET requests
        elif self.request.method == 'POST':
            return [IsAuthenticated(), HasCompleteProfile]  # Specify your desired permission class for POST requests
        return []

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
        


class JobApplicationPage(APIView):
    
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

    def post(self, request, format=None, **kwargs):
        job_id = kwargs.get('id')  # Assuming 'job_id' is a parameter in the URL
        job = Job.objects.get(id=job_id)
        if job.expired == True:
            return Response({"Message": "OOPS!!, Applications are no longer being accepted"}, status=status.HTTP_410_GONE)
        if request.user.is_authenticated:
            user = CustomUser.objects.get(email=request.user)
            print(request.user)
            current_job = Application.objects.create(job=job, first_name=user.profile.first_name, last_name=user.profile.last_name, email=user.email, cv=user.profile.cv, country=user.profile.country)
            serializer = ApplicationsSerialzier(current_job)
            message = {"Success": "Application has been submitted"}
            message.update(serializer.data)
        else:
            current_job = Application(job=job)
            serializer = ApplicationsSerialzier(current_job, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = {"Success": "Application has been submitted"}
            message.update(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED)

            
    

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
    
    def put(self, request, format=None, **kwargs):
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
        
        if request.user != job.posted_by:
            return Response({"Error": "You can't update a job"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = {"Success": "Post update successful"}
            message.update(serializer.data)
            return Response(message, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None, **kwargs):
        slug = kwargs.get("slug")
        id = kwargs.get("id")
        
        try:
            if id:
                job = get_object_or_404(Job, id=id)
            elif slug:
                job = get_object_or_404(slug=slug)
            elif job and slug:
                job = get_object_or_404(id=id, slug=slug)
        except Job.DoesNotExist:
                return Response("Job not found", status=status.HTTP_404_NOT_FOUND)
        
        if request.user != job.posted_by:
            return Response({"Error": "You can't delete this job"}, status=status.HTTP_401_UNAUTHORIZED)
        job.delete()
        return Response({"Success": "Post deletion successful"})
        
        

            
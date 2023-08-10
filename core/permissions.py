from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Job

class CompleteProfilePermission(permissions.BasePermission):
    """
    Custom permission to only allow users with complete profiles to access a view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if the user's profile is complete
        profile = request.user.profile  # Assuming the profile is linked to the User model
        return profile.is_complete
    


class HasPhoneNumberPermission(permissions.BasePermission):
    message = {"You must complete your profile to create, view or accept tasks, click on this link: http://127.0.0.1:8000/users/profile/"}
    def has_permission(self, request, view):
        
        check = bool(request.user.profile.phone_number)
        if check == False:
            raise PermissionDenied(detail=self.message)
        return bool(request.user.profile.phone_number)
    

class CanViewJobApplications(permissions.BasePermission):
    """
    Custom permission to only allow the user who posted a job to view its applications.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        job_id = view.kwargs.get('id')  # Retrieve job ID from the URL'
        job = Job.objects.get(id=job_id)  # Replace with your model and query logic
        return job.posted_by == request.user


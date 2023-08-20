from django.urls import path
from .views import SignUpView, EmployerSignUp

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/employer/", EmployerSignUp.as_view(), name="employer-signup")
]
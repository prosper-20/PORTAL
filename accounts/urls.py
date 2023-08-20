from django.urls import path
from .views import SignUpView, EmployerSignUp, MyAccountView

urlpatterns = [
    path("me/", MyAccountView.as_view(), name="users-me"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/employer/", EmployerSignUp.as_view(), name="employer-signup")
]
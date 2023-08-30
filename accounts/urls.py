from django.urls import path
from .views import (SignUpView, 
                    EmployerSignUp, 
                    MyAccountView, 
                    UserLoginAPIView,
                    ProfileView,
                    AllUsersView,
                    PasswordResetView,
                    ChangePasswordView)

urlpatterns = [
    path("me/", MyAccountView.as_view(), name="users-me"),
    path("me/profile/", ProfileView.as_view(), name="user-profile"),
    path("me/password-reset/", PasswordResetView.as_view(), name='password-reset'),
    path("me/password-change/", ChangePasswordView.as_view(), name="password-change"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", UserLoginAPIView.as_view(), name="signin"),
    path("signup/employer/", EmployerSignUp.as_view(), name="employer-signup"),
    path("all/", AllUsersView.as_view(), name="all-users")
]
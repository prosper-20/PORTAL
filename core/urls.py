from django.urls import path
from .views import JobHomePage, JobDetailPage, ApplicationHomePage


urlpatterns = [
    path("", JobHomePage.as_view(), name="home"),
    path("<uuid:id>/", JobDetailPage.as_view(), name="detail-id"),
    path("<uuid:id>/applications/", ApplicationHomePage.as_view(), name="job-applications"),
    path("<slug:slug>/", JobDetailPage.as_view(), name="detail-slug")
]
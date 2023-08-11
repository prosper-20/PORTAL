from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    job_url = serializers.HyperlinkedIdentityField(view_name="detail-id", lookup_field="id")
    class Meta:
        model = Job
        fields = ["id", "job_url", "title", "slug", "company_name", "salary", "location"]


class ApplicationsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "first_name", "last_name", "email", "cv", "country", "cover_letter", "created"]
from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    job_url = serializers.HyperlinkedIdentityField(view_name="detail-id", lookup_field="id")
    application_url = serializers.SerializerMethodField("get_application_url")
    class Meta:
        model = Job
        fields = ["id", "title", "slug", "company_name", "salary", "location", "job_url", "application_url"]

    def get_application_url(self, obj):
        application_url = f"http://127.0.0.1:8000/jobs/{obj.id}/apply"
        return application_url


class ApplicationsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "first_name", "last_name", "email", "cv", "country", "cover_letter", "created"]
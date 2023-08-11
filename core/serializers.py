from rest_framework import serializers
from .models import Job, Application
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import datetime, timezone

class JobSerializer(serializers.ModelSerializer):
    job_url = serializers.HyperlinkedIdentityField(view_name="detail-id", lookup_field="id")
    application_url = serializers.SerializerMethodField("get_application_url")
    get_job_existence = serializers.SerializerMethodField("get_time_since_created")


    class Meta:
        model = Job
        fields = ["id", "title", "slug", "company_name", "salary", "location", "job_url", "application_url", "get_job_existence"]

    def get_application_url(self, obj):
        application_url = f"http://127.0.0.1:8000/jobs/{obj.id}/apply"
        return application_url

    def get_time_since_created(self, obj):
        now = datetime.now(timezone.utc)
        time_difference = now - obj.date_posted
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"


class ApplicationsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "first_name", "last_name", "email", "cv", "country", "cover_letter", "created"]
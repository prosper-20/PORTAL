from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", "company_name")}
    list_display = ["title", "company_name", "salary"]
    list_filter = ["salary", "location", "expired"]
    list_editable = ["salary"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["job", "first_name", "created"]
    list_filter = ["job", "first_name", "last_name"]
    search_fields = ["job"]




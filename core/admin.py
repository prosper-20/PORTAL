from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "company_name", "salary"]
    list_filter = ["salary", "location", "expired"]
    list_editable = ["salary"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["job", "username", "created"]
    list_filter = ["job", "username"]
    search_fields = ["job"]
    



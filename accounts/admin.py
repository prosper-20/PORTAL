from django.contrib import admin
from .models import CustomUser, Profile



@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]



admin.site.register(Profile)
    


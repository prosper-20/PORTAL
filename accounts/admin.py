from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "date_joined"]
    list_filter = ["is_active"]


admin.site.register(Profile)
    


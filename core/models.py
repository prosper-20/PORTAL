from django.db import models
import uuid
from accounts.models import CustomUser

class Job(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    slug = models.SlugField()
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    responsilbilities = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
COUNTRY_CHOICES = (
    ('Nigeria', 'Nigeria'),
    ('Ethopian', 'Ethopia'),
    ('Germany', 'Germany'),
    )

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    cv = models.FileField(upload_to="applications")
    cover_letter = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.username} application"
    

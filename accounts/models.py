from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .managers import CustomUserManager
import string
import random, os

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default2.jpg",upload_to="account_pics", blank=True)
    bio = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    is_complete = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} profile"

    @property
    def filename(self):
        return os.path.basename(self.image.name)
    



def generate_referral_code():
    # Generate a random referral code
    letters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(letters) for _ in range(6))
    return code

class Referral(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, default=generate_referral_code)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} code"
    





    
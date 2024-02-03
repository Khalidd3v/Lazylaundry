import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email can't be blank")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=self.normalize_email(email), password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class LazyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField(max_length=32, unique=True)
    phone_number = models.IntegerField(blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.username:
            # If username is not provided, generate one
            self.username = self.generate_username()
        super().save(*args, **kwargs)

    def generate_username(self):
        # Generate a random 8-character username
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

        # Check if the generated username already exists
        while LazyUser.objects.filter(username=random_chars).exists():
            random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

        return random_chars

    def __str__(self):
        return self.email

    def has_prem(self, perm, obj=None):
        return self.is_superuser
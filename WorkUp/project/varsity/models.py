from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random, string
import uuid

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
      # Create a standard user
      if not email:
         raise ValueError('The Email field must be set')
      email = self.normalize_email(email)
      user = self.model(email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user

    def create_superuser(self, email, password=None, **extra_fields):
      # Create a superuser
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)

      if extra_fields.get('is_staff') is not True:
         raise ValueError('Superuser must have is_staff=True.')
      if extra_fields.get('is_superuser') is not True:
         raise ValueError('Superuser must have is_superuser=True.')

      return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
   id = models.UUIDField(default=uuid.uuid4, primary_key=True)
   full_name = models.CharField(max_length=200)
   email = models.EmailField(unique=True)
   password = models.CharField(max_length=150)
   # username = models.CharField(max_length=7)
   is_student = models.BooleanField(default=True)
   
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []
   
   objects = CustomUserManager()

   def save(self, *args, **kwargs):
      if not self.username:
         generated_username="".join(random.choices(string.digits + string.ascii_uppercase, k=7))
         self.username = generated_username
         return super().save(*args, **kwargs)
   
   def __str__(self):
      return self.email
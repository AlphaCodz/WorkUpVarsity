from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random, string, uuid


# Create your models here.
class MainUser(AbstractUser):
   id = models.CharField(max_length=36, unique=True, primary_key=True, default=uuid.uuid4)
   full_name = models.CharField(max_length=350)
   email = models.EmailField(unique=True)
   password = models.CharField(max_length=200)
   username = models.CharField(unique=True, max_length=7)
   is_student = models.BooleanField(default=False)
   is_instructor = models.BooleanField(default=False)
   
   EMAIL_FIELD = 'email'
   REQUIRED_FIELDS = []

   def save(self, *args, **kwargs):
      if not self.username:
         new_username = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
         self.username = new_username
      super().save(*args, **kwargs)
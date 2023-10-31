from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random, string, uuid
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# Create your models here.
class MainUser(AbstractUser):
   # Student Data
   id = models.CharField(max_length=36, unique=True, primary_key=True, default=uuid.uuid4)
   full_name = models.CharField(max_length=350)
   email = models.EmailField(unique=True)
   password = models.CharField(max_length=200)
   username = models.CharField(unique=True, max_length=7)
   is_student = models.BooleanField(default=False)
   
   # Instructor Data
   TITLE = (
      ('Mr.', 'Mr.'),
      ('Mrs.', 'Mrs.')
   )
   EXPERIENCE_LEVEL = (
      ('None', 'None'),
      ('1 Year', '1 Year'),
      ('3 Years', '3 Years'),
      ('5 Years', '5 Years'),
      ('7 Years and above', '7 Years and above')
   )
   
   # AOE = Area Of Interest
   AOE = (
      ('Web Development', 'Web Development'),
      ('Graphics Design', 'Graphics Design'),
      ('Web 3', 'Web 3'),
      ('Network Security', 'Network Security'),
      ('Digital Marketing', 'Digital Marketing'),
      ('Frontend Development', 'Frontend Development'),
      ('Backend Development', 'Backend Development'),
      ('Software Development', 'Software Development'),
      ('Embedded Software Engineering', 'Embedded Software Engineering'),
      ('Mobile Application Development', 'Mobile Application Development'),
      ('Graphics Design', 'Graphics Design'),
      ('Database Systems', 'Database Systems'),
      ('Computer Networking', 'Computer Networking'),
      ('Digital/Affiliate Marketing', 'Digital/Affiliate Marketing'),
      ('Other', 'Other')
   )
   
   TYPE = (
      ('Skilled', 'Skilled'),
      ('UnSkilled', 'UnSkilled')
   )
   
   title = models.CharField(max_length=4, choices=TITLE, null=True)
   contact = models.CharField(max_length=11, unique=True, null=True)
   street_address = models.CharField(max_length=20, null=True)
   city = models.CharField(max_length=15, null=True)
   state = models.CharField(max_length=20, null=True)
   country = models.CharField(max_length=25, null=True)
   passport = models.FileField(storage=RawMediaCloudinaryStorage, null=True)
   resume = models.FileField(storage=RawMediaCloudinaryStorage, null=True) 
   years_of_experience = models.CharField(max_length=17, choices=EXPERIENCE_LEVEL, null=True)
   linkedin_profile = models.URLField(null=True)
   area_of_interest = models.CharField(max_length=35, choices=AOE, null=True)
   about_me = models.TextField(null=True)
   is_instructor = models.BooleanField(default=False)
   course_type = models.CharField(choices=TYPE, max_length=9, null=True)
   
   EMAIL_FIELD = 'email'
   REQUIRED_FIELDS = []

   def save(self, *args, **kwargs):
      if not self.username:
         new_username = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
         self.username = new_username
      super().save(*args, **kwargs)
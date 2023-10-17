from django.db import models
from main_app.models import MainUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Course(models.Model):
   name = models.CharField(max_length=300, unique=True)
   description = models.TextField()
   requirements = ArrayField(models.CharField(max_length=100), size=8)
   expectancy = ArrayField(models.CharField(max_length=150), size=8)
   learning_materials = ArrayField(models.CharField(max_length=150), size=8)
   instructor = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, limit_choices_to={'is_instructor':True})
   category = models.OneToOneField('Category', on_delete=models.CASCADE)
   price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
   
   def __str__(self):
      return self.name
   

class Category(models.Model):
   CATEGORY = (
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
   name = models.CharField(max_length=35, unique=True)
   
   def __str__(self):
      return self.name
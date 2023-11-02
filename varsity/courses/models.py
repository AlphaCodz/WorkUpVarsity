from django.db import models
from main_app.models import MainUser
from django.contrib.postgres.fields import ArrayField
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# Create your models here.

class Course(models.Model):
   DIFFICULTY = (
      ('Beginner', 'Beginner'),
      ('Intermediate', 'Intermediate'),
      ('Master', 'Master')
   )
   
   CHARGE_STATUS = (
      ('Free', 'Free'),
      ('Paid', 'Paid')
   )
   
   TYPE = (
      ('Skilled', 'Skilled'),
      ('UnSkilled', 'UnSkilled')
   )
   
   name = models.CharField(max_length=300, unique=True)
   description = models.TextField()
   requirements = models.TextField()
   # expectancy = ArrayField(models.CharField(max_length=150), size=8)
   learning_materials = models.TextField()
   what_to_gain = models.TextField(null=True)
   instructor = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, limit_choices_to={'is_instructor':True})
   # category = models.OneToOneField('Category', on_delete=models.CASCADE)
   price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
   public_course = models.BooleanField(default=False)
   category = models.ForeignKey('Category', on_delete=models.CASCADE)
   q_and_a = models.BooleanField(default=False)
   charge_status = models.CharField(choices=CHARGE_STATUS, max_length=4)
   course_thumbnail = models.FileField(storage=RawMediaCloudinaryStorage, null=True)
   course_type = models.CharField(choices=TYPE, max_length=9, null=True)
   
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


class Topic(models.Model):
   name = models.CharField(max_length=100)
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   summary = models.TextField(null=True)


class Content(models.Model):
   name = models.CharField(max_length=50, null=True)
   topic = models.ManyToManyField(Topic)
   video = models.FileField(storage=RawMediaCloudinaryStorage)
   description = models.TextField(null=True)
   hour = models.IntegerField(null=True)
   minutes = models.IntegerField(null=True)
   seconds = models.IntegerField(null=True)
   
   
class CourseReview(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses")
   student = models.OneToOneField(MainUser, on_delete=models.CASCADE)
   comment = models.TextField()
   rating = models.IntegerField()
   
   def __str__(self):
      return self.student


class CourseOwnership(models.Model):
   student = models.ForeignKey(MainUser, on_delete=models.CASCADE)
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   purchase_date = models.DateTimeField(auto_now_add=True)
   transaction_details = models.TextField()

   def __str__(self):
      return f"{self.user.username} - {self.course.name} Ownership"
   
   
class Question(models.Model):
   user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   text = models.TextField()
   
   def __str__(self):
      return self.user.full_name
   
   
class Reply(models.Model):
   question=models.ForeignKey(Question, on_delete=models.CASCADE)
   user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
   text = models.TextField(null=True)

   def __str__(self):
      return self.user.username

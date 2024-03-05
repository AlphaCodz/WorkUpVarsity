from django.db import models
from main_app.models import MainUser, AffiliateAccount
from django.contrib.postgres.fields import ArrayField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage, RawMediaCloudinaryStorage
import uuid, cloudinary, logging
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from rest_framework import response, status
from decimal import Decimal
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
   price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
   public_course = models.BooleanField(default=False)
   category = models.ForeignKey('Category', on_delete=models.CASCADE)
   q_and_a = models.BooleanField(default=False)
   charge_status = models.CharField(choices=CHARGE_STATUS, max_length=4)
   course_thumbnail = models.URLField()
   course_type = models.CharField(choices=TYPE, max_length=9, null=True)
   published = models.BooleanField(default=False)
   
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
   video = models.URLField(null=True)
   description = models.TextField(null=True)
   duration = models.CharField(max_length=10, null=True)
   content_file = models.URLField(null=True)
   completed = models.BooleanField(default=False)


class CourseReview(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courses")
   student = models.OneToOneField(MainUser, on_delete=models.CASCADE)
   comment = models.TextField()
   rating = models.IntegerField()
   
   def __str__(self):
      return self.student

   
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


class Ebook(models.Model):
   name = models.CharField(max_length=200, unique=True)
   image = models.ImageField(upload_to='ebooks', blank=True)
   description = models.TextField(null=True)
   price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
   url = models.URLField(unique=True, null=True)
   
   def __str__(self):
      return self.name


class MyCourse(models.Model):
   user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='courses')
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   paid = models.BooleanField(default=True)
   purchased_at = models.DateTimeField(auto_now_add=True, null=True)
   

   def __str__(self):
      return f"{self.user.first_name} | {self.course.name}"

   def save(self, *args, **kwargs):
      if self.course:
         user = self.user
         course = self.course
         amount_earned = Decimal(course.price) * Decimal('0.20')
         
         referee = self.get_referee(user)
         # print(referee)
         if referee is not None:
            affiliate = AffiliateAccount.objects.get(user=referee)
            affiliate.balance += amount_earned
            affiliate.save()
         else:
            pass
      super().save(*args, **kwargs)

   def get_referee(self, user):
      """
      Get User's Referee if available
      """
      try:
         referee = MainUser.objects.get(id=user.id)
         ref_id = referee.referred_by
         if ref_id:
               referee_instance = MainUser.objects.get(affiliate_code=ref_id)
               return referee_instance
      except MainUser.DoesNotExist:
         return None  # Return None when user is not found


class MyEbooks(models.Model):
   user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name = 'ebooks')
   ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
   paid = models.BooleanField(default=True)
   purchased_at = models.DateTimeField(auto_now_add=True)
   
class State(models.Model):
   name = models.CharField(max_length=30, unique=True)
   delivery_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
   
   
class Order(models.Model):
   id=models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
   buyer = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True)
   address = models.CharField(max_length=250, null=False)
   contact = models.CharField(max_length=15, null=True)
   state = models.ForeignKey(State, on_delete=models.DO_NOTHING)
   total_price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
   created_at = models.DateTimeField(auto_now_add=True)
   
   
class OrderItems(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
   items = models.ForeignKey("main_app.ShopProduct", on_delete=models.CASCADE, null=True, related_name='products')
   quantity = models.IntegerField(default=1)
   
   def clean(self):
      if self.quantity < 1:
         raise ValidationError("Quantity Cannot be less than 1")

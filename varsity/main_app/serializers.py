from rest_framework import serializers, validators
from main_app.models import MainUser
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class SignUpStudentSerializer(serializers.ModelSerializer):
   class Meta:
      model = MainUser
      fields = ["id", "full_name", "email", "username", "password"]
      read_only_fields = ["id", "username"]

   def validate_password(self, value):
      # Password Security
      if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).+$', value):
         raise serializers.ValidationError("Passwords must include at least one special symbol, one number, one lowercase letter, and one uppercase letter.")
      return value

   def create(self, validated_data):
      password = validated_data.get('password')
      
      # Validate password using the validate_password method
      self.validate_password(password)
      
      # Assign student to DB
      student = MainUser(**validated_data)
      student.is_student = True #Confirm Student Status
      
      # Use set_password to hash the password
      student.set_password(password)
      
      student.save()  # Save student data after setting password
      return student

         
class SignUpInstructorSerializer(serializers.ModelSerializer):
   # full name,last name, email,username,years of experience,country,city,contact
   class Meta:
      model = MainUser
      fields = ["id", "full_name", "email", "username", "password", "contact", "street_address", "city", "state", "country", "linkedin_profile", "years_of_experience", "area_of_interest", "about_me", "resume", "passport"]
      read_only_fields = ["id"]
      
      extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True},
            'username': {'required': True},
            'years_of_experience': {'required': False},
            'country': {'required': True},
            'city': {'required': False},
            'contact': {'required': False},
            'street_address': {'required':False},
            'city': {'required':False},
            'state': {'required': False},
            'country': {'required': False},
            'linkedin_profile': {'required': False},
            'years_of_experience': {'required': False},
            'area_of_interest': {'required': False},
            'about_me': {'required': False},
            'resume': {'required': False},
            'password': {'required': False},
      }

   def validate_password(self, value):
      # Password Security
      if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).+$', value):
         raise serializers.ValidationError("Passwords must include at least one special symbol, one number, one lowercase letter, and one uppercase letter.")
      return value

   def create(self, validated_data):
      password = validated_data.get('password')
      
      # Validate password using the validate_password method
      self.validate_password(password)
      
      # Assign student to DB
      instructor = MainUser(**validated_data)
      instructor.is_instructor = True 
      
      # Use set_password to hash the password
      instructor.set_password(password)
      
      instructor.save()  # Save student data after setting password
      return instructor

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   username_field = MainUser.USERNAME_FIELD

   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)
      token['email'] = user.email
      return token

   def validate(self, attrs):
      data = super().validate(attrs)
      user = self.user

      if user and user.is_authenticated:
         data['user_data'] = {
               "id": user.id,
               "first_name": user.full_name,
               "email": user.email,
               "username": user.username,
               "is_student": user.is_student,
         }

         if not user.is_student:
               data['user_data'].update({
                  "is_instructor": user.is_instructor,
                  "passport": getattr(user.passport, 'url()', lambda: None)(),
                  "title": user.title,
                  "contact": user.contact,
                  "street_address": user.street_address,
                  "city": user.city,
                  "state": user.state,
                  "country": user.country,
                  "resume": getattr(user.resume, 'url()', lambda: None)(),
                  "years_of_experience": user.years_of_experience,
                  "linkedin_profile": user.linkedin_profile,
                  "area_of_interest": user.area_of_interest,
                  "about_me": user.about_me,
               })

         refresh = self.get_token(user)
         data["refresh"] = str(refresh)
         data["access"] = str(refresh.access_token)
         return data
      else:
         raise serializers.ValidationError("No active account found with the given credentials")

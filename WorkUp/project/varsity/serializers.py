from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
import re

class SignUpStudent(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ("id", "username","full_name", "email", "password")
      read_only_fields = ("id", "username",)
      
      
   class SignUpStudent(serializers.ModelSerializer):
      class Meta:
         model = User
         fields = ("id", "username", "full_name", "email", "password")
         read_only_fields = ("id", "username",)
   
   def create(self, validated_data):
      # Extract password from validated_data
      password = validated_data.get("password")

      # Validate the password using regular expressions
      if password and not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).+$', password):
         raise serializers.ValidationError({
               "error": "Passwords must include at least one special symbol, one number, one lowercase letter, and one uppercase letter."
         })

      # Create the user without saving it yet
      user = User(**validated_data)
      user.is_student = True

      if password:
         # Set and save the user's password only if a valid password is provided
         user.set_password(password)

      user.save()  # Save the user after setting the password
      return user
   

class SignInStudent(TokenObtainPairSerializer):
   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)
      token['email'] = user.email
      return token
   
   def validate(self, attrs):
      data = super().validate(attrs)
      data['user_data'] = {
         'id': self.user.id,
         'full_name': self.user.full_name,
         'email': self.user.email,
         'is_student': self.user.is_student
      }
      refresh = self.get_token(self.user)
      data['refresh'] = str(refresh)
      data['access'] = str(refresh.access_token)
      return data
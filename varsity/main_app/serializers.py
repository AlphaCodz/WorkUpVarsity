from rest_framework import serializers, validators
from main_app.models import MainUser, ShopProduct, AffiliateAccount
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from courses.models import Course
from main_app.payment_model import RecipientHoldingAccount

class SignUpStudentSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True, style={'input_type': 'password'})
   referred_by = serializers.CharField(required=False)
   affiliate_code = serializers.CharField(read_only=True)
   affiliate_balance = serializers.CharField(read_only=True)
   

   class Meta:
      model = MainUser
      fields = ["id", "full_name", "email", "username", "affiliate_code","status", "referred_by", "password", "affiliate_balance"]
      read_only_fields = ["id", "username", "affiliate_code"]

   def validate_password(self, value):
      # Password Security
      if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).+$', value):
         raise serializers.ValidationError("Passwords must include at least one special symbol, one number, one lowercase letter, and one uppercase letter.")
      return value

   def create(self, validated_data):
      password = validated_data.pop('password', None)

      # Validate password using the validate_password method
      self.validate_password(password)

      # Assign student to DB
      student = MainUser(**validated_data)
      student.is_student = True  # Confirm Student Status

      # Use set_password to hash the password
      student.set_password(password)
      student.save()  # Save student data after setting password

      # Process affiliate code
      referred_by = validated_data.get('referred_by')
      print(referred_by)
      if referred_by:
         self.process_affiliate(referred_by)
      return student

   def process_affiliate(self, code):
      if code:
         try:
            user = MainUser.objects.get(affiliate_code=code)
         except MainUser.DoesNotExist:
            raise serializers.ValidationError("Incorrect Code", 404)
         
         beneficiary = user.id
         print(beneficiary)
         
         # Add Bonus to Affiliate
         account = AffiliateAccount.objects.get(user=beneficiary)
         account.balance += 100
         account.save()
         print(f"{beneficiary} Paid Successfully")

   def to_representation(self, instance):
      representation = super(SignUpStudentSerializer, self).to_representation(instance)
      representation["affiliate_balance"] = self.get_balance(instance.pk)
      return representation

   def get_balance(self, user_id):
      try:
         affiliate = AffiliateAccount.objects.get(user=user_id)
      except AffiliateAccount.DoesNotExist:
         return 0.00
      return affiliate.balance
   
class SignUpInstructorSerializer(serializers.ModelSerializer):
   # full name,last name, email,username,years of experience,country,city,contact
   instructor_course_data = serializers.CharField(read_only=True)
   class Meta:
      model = MainUser
      fields = ["id", "full_name", "email", "username", "password", "contact", "street_address", "city", "state", "country", "linkedin_profile", "years_of_experience", "area_of_interest", "about_me", "resume", "passport", "instructor_course_data"]
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
   
   def to_representation(self, instance):
      representation = super(SignUpInstructorSerializer, self).to_representation(instance)
      representation['instructor_course_data'] = {
         "no_of_course": self.get_instructor_course(instance.id)
      }
      return representation
   
   def get_instructor_course(self, instructor_id):
      try:
         verified_instructor = MainUser.objects.get(id=instructor_id)
      except MainUser.DoesNotExist:
         raise serializers.ValidationError("Instructor Does Not Exist", code=404)
      
      # Get Instructors Course Counts
      try:
         course_count = Course.objects.filter(instructor=verified_instructor).count()
      except Course.DoesNotExist:
         return []
      
      return course_count


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
               "full_name": user.full_name,
               "email": user.email,
               "username": user.username,
               "is_student": user.is_student,
               "status": user.status
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


class ShopSerializers(serializers.ModelSerializer):
   class Meta:
      model = ShopProduct
      fields = ['id', 'name', 'price', 'image']
      

class RecipientHoldingAccountSerializer(serializers.ModelSerializer):
   class Meta:
      model = RecipientHoldingAccount
      fields = ['id', 'user', 'account_number', 'name', 'bank_code']
   
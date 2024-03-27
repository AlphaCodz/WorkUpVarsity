from django.shortcuts import render
from .serializers import SignUpStudentSerializer, SignUpInstructorSerializer, MyTokenObtainPairSerializer, RecipientHoldingAccountSerializer, AffiliateBalanceSerializer
from .models import MainUser, AffiliateAccount
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .payment_model import RecipientHoldingAccount
from rest_framework import status, views
from rest_framework.response import Response
from .permissions import SuperPermission
import logging

# Create your views here.
class SignUpStudent(ModelViewSet):
   queryset = MainUser.objects.all().order_by('-date_joined')
   serializer_class = SignUpStudentSerializer
   permission_classes = (AllowAny, )


# Instructor Account Registration
class SignUpInstructor(ModelViewSet):
   queryset = MainUser.objects.filter(is_instructor=True)
   serializer_class = SignUpInstructorSerializer
   permission_classes = (AllowAny, )


class SignInUserView(TokenObtainPairView):
   permission_classes = (AllowAny, )
   serializer_class = MyTokenObtainPairSerializer
   
   
class CreateHoldingAccount(ModelViewSet):
   queryset = RecipientHoldingAccount.objects.select_related('user')
   serializer_class = RecipientHoldingAccountSerializer
   

class MyReferredUsersView(ViewSet):
   def list(self, request):
      user_id = self.request.query_params.get("user")
      try:
         verified_user = self.get_user(user_id)
         affiliate_code = self.get_affiliate_code(verified_user)
         referred_users = MainUser.objects.filter(referred_by=affiliate_code)
      except MainUser.DoesNotExist:
         return Response("User or Affiliate Does Not Exist", status=status.HTTP_404_NOT_FOUND)

      data = [{"name": referee.full_name, "amount_earned": "100.00"} for referee in referred_users.all()]
      return Response(data, status=status.HTTP_200_OK)

   def get_user(self, user_id):
      try:
         user = MainUser.objects.get(id=user_id)
      except MainUser.DoesNotExist:
         return Response("User Not Found", status=status.HTTP_404_NOT_FOUND)
      return user

   def get_affiliate_code(self, user):
      # Assuming user is already an instance of MainUser
      return user.affiliate_code
      

class UpdatePassword(views.APIView):
   def post(self, request):
      email = request.data.get("email")
      new_password = request.data.get("new_password")
      
      if not email or not new_password:  # Check if email and new_password are provided
         return Response("Email and new password are required", status=status.HTTP_400_BAD_REQUEST)
      
      verified_user = self.verify_user_exists(email)
      if not verified_user:
         return Response("Email with this account does not exist", status=status.HTTP_400_BAD_REQUEST)
      
      verified_user.set_password(new_password)
      verified_user.save()
      
      return Response("Password Updated Successfully!", status=status.HTTP_200_OK)
   
   
   def verify_user_exists(self, email):
      try:
         user = MainUser.objects.get(email=email)
         return user
      except MainUser.DoesNotExist:
         return None


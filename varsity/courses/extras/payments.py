import requests
from main_app.models import MainUser, RecipientAccount, AffiliateAccount
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from decimal import Decimal


def get_user_or_none(user_id):
   try:
      return get_user_model().objects.get(id=user_id, is_instructor__in=[True, False])
   except get_user_model().DoesNotExist:
      return None

def get_recipient_account(user_id):
   try:
      return RecipientAccount.objects.get(user=user_id)
   except RecipientAccount.DoesNotExist:
      return None
   


class MakePayment(APIView):
   @csrf_exempt
   @transaction.atomic
   def post(self, request: HttpRequest):
      user_id = request.POST.get("user")
      
      # VERIFY USER EXISTENCE
      user_exists = get_user_or_none(user_id)
      
      if user_exists:
         # Process your payment logic here
         payment_response = self.process_payment(request)
         return payment_response
      else:
         return Response({"message": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

   @transaction.atomic
   def process_payment(self, request: HttpRequest):
      url = "https://api.paystack.co/transaction/initialize"
      headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {settings.TEST_SECRET_KEY}'
      }
      # Get User Data
      user = self.collect_user(request)
      amount = self.request.data.get("amount")
      actual_amount = int(amount) * 100

      payload = {
         "email": user.email,
         "amount": actual_amount,
         "channels": ["card"]
      }

      response = requests.post(url, headers=headers, json=payload)
      if response.status_code == 200:
         data = response.json()
         return Response(data, status=status.HTTP_200_OK)
      else:
         return Response({"message": f"{response.text}"}, status=response.status_code)

   def collect_user(self, request: HttpRequest):
      user_id = request.data.get("user")
      user_exists = get_user_or_none(user_id)
      if user_exists:
         return user_exists
      else:
         raise ValueError("Invalid User ID.")


class VerifyPayment(APIView):
   def get(self, request):
      # Use QueryDict to get query parameters
      reference = self.request.query_params.get("reference")

      headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {settings.TEST_SECRET_KEY}'
      }

      url = f"https://api.paystack.co/transaction/verify/{reference}"

      response = requests.get(url, headers=headers)

      if response.status_code == 200:
         response_data = response.json()
         return Response(response_data, status=status.HTTP_200_OK)
      else:
         response_data = response.text
         return Response({"message": f'{response_data}'}, status=response.status_code)
      
      
class InitiateTransfer(APIView):
   @csrf_exempt
   @transaction.atomic
   def post(self, request: HttpRequest):
      user_id = request.POST.get("user")
      
      # VERIFY USER EXISTENCE
      user_exists = get_user_or_none(user_id)
      
      recipient_exists = get_recipient_account(user_id)
      
      if user_exists and recipient_exists:
         # Process your payment logic here
         transfer_response = self.initiate_transfer(request)
         return transfer_response
      else:
         return Response({"message": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)
      
   @transaction.atomic
   def initiate_transfer(self, request: HttpRequest):
      url = "https://api.paystack.co/transferrecipient"
      headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {settings.TEST_SECRET_KEY}'
      }

      data = {
         "type": "nuban",
         "name": self.collect_user(request).user.full_name,
         "account_number": int(self.collect_user(request).account_number),
         "bank_code": int(self.collect_user(request).bank_code),
         "currency": "NGN"
      }

      try:
         response = requests.post(url, json=data, headers=headers)
         response_data = response.json()

         return Response(response_data, status=status.HTTP_200_OK)

      except requests.RequestException as e:
         return Response(str(response_data.text), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
      
   def collect_user(self, request: HttpRequest):
      user_id = request.data.get("user")
      user_exists = get_recipient_account(user_id)
      if user_exists:
         return user_exists
      else:
         raise ValueError("Invalid User ID.")
      
      
class MakeTransfer(APIView):
   @transaction.atomic
   def post(self, request: HttpRequest):
      url = "https://api.paystack.co/transfer"
      headers = {
         'Content-Type': 'application/json',
         'Authorization': f'Bearer {settings.TEST_SECRET_KEY}'
      }
      amount = request.data.get("withdrawal_amount")
      recipient = request.data.get("recipient_code")

      verified_amount = self.validate_amount(request, amount)

      data = {
         "source": "balance",
         "reason": "Congratulations! WorkUpVarsity Affiliate Payment is here.",
         "amount": verified_amount,
         "recipient": recipient
      }
      
      try:
         response = requests.post(url, json=data, headers=headers)
         response_data = response.json()

         return Response(response_data, status=status.HTTP_200_OK)

      except requests.RequestException as e:
         return Response(str(response_data.text), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   def validate_amount(self, request, withdrawal_amount):
      user_id = request.data.get("user")

      # Check Affiliate Balance
      affiliate = get_object_or_404(AffiliateAccount, user=user_id)
      balance = affiliate.balance
      print(balance)

      withdrawal_amount_decimal = Decimal(withdrawal_amount)

      # if balance < withdrawal_amount_decimal:
      #    raise ValidationError("Insufficient Funds", code=status.HTTP_400_BAD_REQUEST)
      # else:
      #    # Update the balance
      balance -= withdrawal_amount_decimal
      affiliate.balance = balance
      affiliate.save()

      return int(withdrawal_amount_decimal)
         
         
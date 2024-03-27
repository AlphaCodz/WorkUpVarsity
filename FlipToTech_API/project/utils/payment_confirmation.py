from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class PaystackVerifyAPIView(APIView):
   def get(self, request, reference, format=None):
      url = f"https://api.paystack.co/transaction/verify/{reference}"
      authorization = "Bearer sk_test_8bf0c5575575a946142b892294b33cc28dbf57f9"

      headers = {
         'Authorization': authorization,
      }

      try:
         response = requests.get(url, headers=headers)
         response.raise_for_status()
         data = response.json()
         # Process the response data as needed
         return Response(data)
      except requests.exceptions.HTTPError as errh:
         return Response({"error": f"HTTP Error: {errh}"}, status=response.status_code)
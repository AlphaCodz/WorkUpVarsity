from .models import MainUser
from django.db import models

class RecipientHoldingAccount(models.Model):
   user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='recipient')
   account_number = models.CharField(max_length=12, unique=True)
   name = models.CharField(max_length=300, null=False)
   bank_code = models.CharField(max_length=7, null=True)
   
   class Meta:
      db_table = 'payment_model_recipientholdingaccount'
      app_label = 'main_app'

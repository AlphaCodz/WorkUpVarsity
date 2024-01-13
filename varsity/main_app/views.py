from django.shortcuts import render
from .serializers import SignUpStudentSerializer, SignUpInstructorSerializer, MyTokenObtainPairSerializer, RecipientHoldingAccountSerializer
from .models import MainUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .payment_model import RecipientHoldingAccount

# Create your views here.
class SignUpStudent(ModelViewSet):
   queryset = MainUser.objects.all()
   serializer_class = SignUpStudentSerializer
   permission_classes = (AllowAny, )

# Instructor Account Registration
class SignUpInstructor(ModelViewSet):
   queryset = MainUser.objects.all()
   serializer_class = SignUpInstructorSerializer
   permission_classes = (AllowAny, )


class SignInUserView(TokenObtainPairView):
   permission_classes = (AllowAny, )
   serializer_class = MyTokenObtainPairSerializer
   
   
class CreateHoldingAccount(ModelViewSet):
   queryset = RecipientHoldingAccount.objects.select_related('user')
   serializer_class = RecipientHoldingAccountSerializer
   


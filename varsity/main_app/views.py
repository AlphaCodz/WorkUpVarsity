from django.shortcuts import render
from .serializers import SignUpStudentSerializer
from .models import MainUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

# Create your views here.
class SignUpStudent(ModelViewSet):
   queryset = MainUser.objects.all()
   serializer_class = SignUpStudentSerializer
   permission_classes = (AllowAny, )
   

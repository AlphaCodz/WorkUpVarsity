from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .models import User
from .serializers import SignUpStudent, SignInStudent

# Create your views here.

class SignUpStudentViewset(ModelViewSet):
   queryset = User.objects.all()
   serializer_class = SignUpStudent


class SignInStudentView(TokenObtainPairView):
   permission_classes = (permissions.AllowAny,)
   serializer_class = SignInStudent

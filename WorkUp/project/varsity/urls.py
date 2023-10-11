from django.urls import path
from .views import SignInStudentView

urlpatterns = [
   path('signin', SignInStudentView.as_view(), name="signin")
]

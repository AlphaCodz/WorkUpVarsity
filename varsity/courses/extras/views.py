from courses.models import MyCourse
from courses.serializers import BuyCourseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

class BuyCourseView(ModelViewSet):
   queryset = MyCourse.objects.select_related("user", "course")
   serializer_class = BuyCourseSerializer
   # lookup_field = "user"
   
   # def get_queryset(self):
   #     return MyCourse.objects.filter("")
   
class MyCourses(generics.ListAPIView):
   serializer_class = BuyCourseSerializer

   def get_queryset(self):
      user = self.kwargs['user']
      return MyCourse.objects.filter(user=user)
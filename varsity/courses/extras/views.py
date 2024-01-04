from courses.models import MyCourse, Reply
from courses.serializers import BuyCourseSerializer, ReplySerializer
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
   
   
class ReplyByCourseView(generics.ListAPIView):
   serializer_class = ReplySerializer

   def get_queryset(self):
      course_id = self.kwargs['course_id']
      return Reply.objects.filter(question__course_id=course_id)
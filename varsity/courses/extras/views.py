from courses.models import MyCourse, Reply, Course, Ebook, Order, MyEbooks
from courses.serializers import BuyCourseSerializer, ReplySerializer, OrderSerializer, BuyEbookSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, views, response, status
from main_app.models import MainUser



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
   
   
class BuyEbookView(ModelViewSet):
   queryset = MyEbooks.objects.select_related('user', 'ebook').order_by('-purchased_at')
   serializer_class = BuyEbookSerializer


class MyEbooksView(generics.ListAPIView):
   serializer_class = BuyEbookSerializer
   
   def get_queryset(self):
      user = self.kwargs['user']
      return MyEbooks.objects.select_related('user', 'ebook').filter(user=user).order_by('-purchased_at')
   
   
   
class ReplyByCourseView(generics.ListAPIView):
   serializer_class = ReplySerializer

   def get_queryset(self):
      course_id = self.kwargs['course_id']
      return Reply.objects.filter(question__course_id=course_id)
   
   
class AdminDashboardCounts(views.APIView):
   def get(self, request):
      # Queries
      course = Course.objects.select_related("instructor", "category")
      ebooks = Ebook.objects.all()
      students = MainUser.objects.filter(is_student=True)
      
      data = {
         "no_of_courses": course.count(),
         "no_of_ebooks": ebooks.count(),
         "no_of_students": students.count()
      }
      
      return response.Response(data, status=status.HTTP_200_OK)
   
   
class MakeOrder(ModelViewSet):
   queryset = Order.objects.select_related('state', 'buyer').order_by('-created_at')
   serializer_class = OrderSerializer
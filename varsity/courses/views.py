from django.shortcuts import render
from .serializers import CourseSerializers, ContentSerializer, TopicSerializer, CourseReviewSerialiazer, CourseOwnerShipSerializer, CategorySerializer, QuestionSerializer, ReplySerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Course, Content, Topic, CourseReview, CourseOwnership, Category, Question, Reply
from main_app.models import MainUser
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Subquery, OuterRef


# Create your views here.
class CreateCourse(ModelViewSet):
   queryset = Course.objects.select_related('category', 'instructor')
   serializer_class = CourseSerializers


class CreateCourseContent(ModelViewSet):
   queryset = Content.objects.prefetch_related('topic')
   serializer_class = ContentSerializer
   

class CreateCourseTopic(ModelViewSet):
   queryset = Topic.objects.select_related('course')
   serializer_class = TopicSerializer


class ReviewCourse(ModelViewSet):
   queryset = CourseReview.objects.select_related('course', 'student')
   serializer_class = CourseReviewSerialiazer
   
   
class CourseOwnerShipView(ModelViewSet):
   queryset = CourseOwnership.objects.select_related('student', 'course')
   serializer_class = CourseOwnerShipSerializer
   

class CreateCourseCategory(ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   
   
class CourseQuestion(ModelViewSet):
   queryset = Question.objects.all().select_related('user', 'course')
   serializer_class = QuestionSerializer


class CourseQuestionReply(ModelViewSet):
   queryset = Reply.objects.all().select_related('question', 'user')
   serializer_class = ReplySerializer
   
   

class MyCourse(ListAPIView):
   def list(self, request):
      instructor_id = request.data.get("instructor")
      verified_instructor = self.get_instructor(instructor_id)

      try:
         courses = Course.objects.filter(instructor=verified_instructor).select_related('instructor', 'category').values("id", "name", "description")
         
         # Fetch average ratings using Subquery
         course_ratings = CourseReview.objects.filter(course=OuterRef('id')).values('course').annotate(avg_rating=Avg('rating')).values('avg_rating')[:1]

         # Add average ratings to the course data
         for course in courses:
               course['avg_rating'] = CourseReview.objects.filter(course=course['id']).aggregate(avg_rating=Avg('rating'))['avg_rating']

         data = {
               "courses": courses
         }
         return Response(data, status=status.HTTP_200_OK)
      except Course.DoesNotExist:
         return Course.objects.none

   def get_instructor(self, instructor_id):
      return get_object_or_404(MainUser, id=instructor_id)
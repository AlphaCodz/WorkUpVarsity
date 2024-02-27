from django.shortcuts import render
from .serializers import CourseSerializers, ContentSerializer, TopicSerializer, CourseReviewSerialiazer, CategorySerializer, QuestionSerializer, ReplySerializer, BuyCourseSerializer, StateSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import (Course, Content, Topic, CourseReview, Category, Question, Reply, MyCourse, State)
from main_app.models import MainUser
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Subquery, OuterRef
from .custom_serializers.serializers import CourseDetailSerializer
from .models import MyCourse
from varsity import settings


class CreateCourse(ModelViewSet):
   queryset = Course.objects.filter(published=True).select_related('category', 'instructor')
   serializer_class = CourseSerializers
   filter_backends = [filters.SearchFilter]
   search_fields = ["name", "category__name"]


class CreateCourseContent(ModelViewSet):
   queryset = Content.objects.prefetch_related('topic')
   serializer_class = ContentSerializer
   

class CreateCourseTopic(ModelViewSet):
   queryset = Topic.objects.select_related('course')
   serializer_class = TopicSerializer


class ReviewCourse(ModelViewSet):
   queryset = CourseReview.objects.select_related('course', 'student')
   serializer_class = CourseReviewSerialiazer


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


class TopicsByCourseView(APIView):
   def get(self, request, *args, **kwargs):
      course_id = kwargs.get("course_id")
      try:
         # Assuming 'course_id' is a valid integer
         course_id = int(course_id)
         
         # Retrieve topics for the given course ID
         topics = Topic.objects.filter(course_id=course_id)

         # Serialize the topics
         serializer = TopicSerializer(topics, many=True)

         return Response(serializer.data)

      except ValueError:
         # Handle the case where 'course_id' is not a valid integer
         return Response({"error": "Invalid course ID"}, status=400)


class CourseTopicsAndContentsAPIView(APIView):
   def get(self, request, pk, format=None):
      try:
         course = Course.objects.get(pk=pk)
      except Course.DoesNotExist:
         return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

      topics = Topic.objects.filter(course=course)
      topic_data = []
      for topic in topics:
         content_data = []
         contents = Content.objects.filter(topic=topic)
         for content in contents:
               content_serializer = ContentSerializer(content)
               content_data.append(content_serializer.data)

         topic_serializer = TopicSerializer(topic)
         topic_data.append({
               "topic": topic_serializer.data,
               "contents": content_data
         })

      course_data = {
         "id": course.id,
         "name": course.name,
         "description": course.description,
         "requirements": course.requirements,
         "learning_materials": course.learning_materials,
         "topics": topic_data
      }

      return Response(course_data, status=status.HTTP_200_OK)
   
   
class StateView(ModelViewSet):
   queryset = State.objects.all()
   serializer_class = StateSerializer
   pagination_class = None
   
   
class APIKEY(APIView):
   def get(self, request):
      API_KEY = {
         'test_key': settings.TEST_SECRET_KEY
      }
      return Response(API_KEY, status=status.HTTP_200_OK)
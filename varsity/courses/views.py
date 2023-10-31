from django.shortcuts import render
from .serializers import CourseSerializers, ContentSerializer, TopicSerializer, CourseReviewSerialiazer, CourseOwnerShipSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Course, Content, Topic, CourseReview, CourseOwnership
from rest_framework import status

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
   
   # def perform_create(self, serializer):
   #    if self.request.user.is_authenticated:
   #       course_ownership = serializer.save(student=self.request.user)
   #       course_ownership.save()  # Ensure the instance is saved to the database
   #    else:
   #       return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
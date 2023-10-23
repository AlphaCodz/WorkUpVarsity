from django.shortcuts import render
from .serializers import CourseSerializers, ContentSerializer, TopicSerializer, CourseReviewSerialiazer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Course, Content, Topic, CourseReview

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
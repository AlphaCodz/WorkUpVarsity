from django.shortcuts import render
from .serializers import CourseSerializers, ContentSerializer, TopicSerializer, CourseReviewSerialiazer, CourseOwnerShipSerializer, CategorySerializer, QuestionSerializer, ReplySerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Course, Content, Topic, CourseReview, CourseOwnership, Category, Question, Reply
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
   

class CreateCourseCategory(ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   
   
class CourseQuestion(ModelViewSet):
   queryset = Question.objects.all().select_related('user', 'course')
   serializer_class = QuestionSerializer


class CourseQuestionReply(ModelViewSet):
   queryset = Reply.objects.all().select_related('question', 'user')
   serializer_class = ReplySerializer
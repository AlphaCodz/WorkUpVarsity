from rest_framework import generics, serializers, viewsets, status
from rest_framework.response import Response
from courses.models import Course, Topic, Content

class ContentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Content
      fields = ('id', 'name', 'description', 'hour', 'minutes', 'seconds', 'content_file')

class TopicSerializer(serializers.ModelSerializer):
   contents = ContentSerializer(many=True, read_only=True)

   class Meta:
      model = Topic
      fields = ('id', 'name', 'summary', 'contents')

class CourseDetailSerializer(serializers.ModelSerializer):
   topics = TopicSerializer(many=True, read_only=True)

   class Meta:
      model = Course
      fields = ('id', 'name', 'description', 'requirements', 'learning_materials', 'what_to_gain', 'instructor',
               'price', 'public_course', 'category', 'q_and_a', 'charge_status', 'course_thumbnail', 'course_type',
               'topics')

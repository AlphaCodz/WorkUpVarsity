from .models import Course, Category, Topic, Content, CourseReview
from main_app.models import MainUser
from rest_framework import serializers
from django.shortcuts import get_object_or_404, Http404
import logging

class CourseReviewSerialiazer(serializers.ModelSerializer):
   class Meta:
      model = CourseReview
      fields = "__all__"
      
      
class CourseSerializers(serializers.ModelSerializer):
   ratings = CourseReviewSerialiazer(many=True, read_only=True)
   
   class Meta:
      model = Course
      fields = ['id', 'name', 'description', 'requirements', 'learning_materials', 'instructor', 'category', 'price', 'public_course', 'q_and_a', 'charge_status', 'course_thumbnail', 'ratings']
      
   def validate(self, attrs):
      category = attrs.get('category')
      instructor = attrs.get('instructor')
      
      if category:
         try:
            cat = get_object_or_404(Category, id=category.id)
         except Exception as e:
            logging.error("An Error as Unexpectedly Occured")
            raise serializers.ValidationError({'message': f'Category ID {category} does not exist.'})
      
      if instructor:
         try:
            tutor = get_object_or_404(MainUser, id=instructor.id)
         except Exception as e:
            logging.error("An Error as Unexpectedly Occured")
            raise serializers.ValidationError({'message': f'Instructor with ID {instructor} does not exist.'})
      return attrs
   
   def to_representation(self, instance):
      representation = super().to_representation(instance)
      representation['category'] = {'id': instance.category.id, 'name': instance.category.name}
      representation['instructor'] = {'id': instance.instructor.id, 'name': instance.instructor.full_name}
      return representation
   
   
class TopicSerializer(serializers.ModelSerializer):
   class Meta:
      model = Topic
      fields = "__all__"
      
   def to_representation(self, instance):
      representation = super().to_representation(instance)
      representation['course'] = {"id": instance.course.id, "name": instance.course.name}
      return representation
      

class ContentSerializer(serializers.ModelSerializer):
   # topic = TopicSerializer(many=True)
   class Meta:
      model = Content
      fields = "__all__"
      
   def to_representation(self, instance):
      representation = super().to_representation(instance)
      representation['topic'] = [{"id": topic.id, "name": topic.name} for topic in instance.topic.all()]
      return representation

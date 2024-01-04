from .models import Course, Category, Topic, Content, CourseReview, MyCourse
from main_app.models import MainUser
from rest_framework import serializers
from django.shortcuts import get_object_or_404, Http404
import logging
from .models import Question, Reply, Ebook, MyEbooks
from datetime import datetime

class CourseReviewSerialiazer(serializers.ModelSerializer):
   class Meta:
      model = CourseReview
      fields = "__all__"
      
   def to_representation(self, instance):
      representation = super().to_representation(instance)
      representation['course'] = {"id": instance.course.id, "name":instance.course.name}
      representation['student'] = {"id": instance.student.id, "name": instance.student.full_name}
      return representation
      
      
class CourseSerializers(serializers.ModelSerializer):
   ratings = CourseReviewSerialiazer(many=True, read_only=True)
   
   class Meta:
      model = Course
      fields = ['id', 'name', 'description', 'requirements', 'learning_materials', 'instructor', 'category', 'price', 'public_course', 'q_and_a', 'charge_status', 'course_thumbnail', 'ratings', 'course_type']
      
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
      representation['topic'] = [{"id": topic.id, "name": topic.name, "summary": topic.summary, "course": self.get_course_by_topic(topic.id)} for topic in instance.topic.all()]
      return representation
   
   def get_course_by_topic(self, topic_id):
      try:
         topic = Topic.objects.get(id=topic_id)
      except Topic.DoesNotExist:
         raise serializers.ValidationError("Topic Does Not Exist")
      topic_data = {"id": topic.course.id, "name": topic.course.name}
      return topic_data


class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model= Category
      fields = "__all__"


# Q & A 
class QuestionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Question
      fields = "__all__"
   
   def to_representation(self, instance):
      representation = super(QuestionSerializer, self).to_representation(instance)
      representation['question'] = instance.text
      representation['course'] = instance.course.name
      representation['user'] = instance.user.full_name
      return representation
      

class ReplySerializer(serializers.ModelSerializer):
   class Meta:
      model = Reply
      fields = "__all__"
      
   def to_representation(self, instance):
      representation = super(ReplySerializer, self).to_representation(instance)
      representation['question'] = {"id": instance.question.id, "text": instance.question.text}
      representation['text'] = instance.text
      representation['user'] = instance.user.full_name
      return representation
      

class EbookSerializer(serializers.ModelSerializer):
   class Meta:
      model = Ebook
      fields = "__all__"


class BuyCourseSerializer(serializers.ModelSerializer):
   purchased_at = serializers.DateTimeField(format="%H:%M%p %Y-%m-%d", read_only=True)

   class Meta:
      model = MyCourse
      fields = ['user', 'course', 'purchased_at', 'paid']
      read_only_fields = ['paid', 'purchased_at']
      
      
   def to_representation(self, instance):
      representation = super(BuyCourseSerializer, self).to_representation(instance)
      representation['course'] = {"id": instance.course.id, "name": instance.course.name, "image": instance.course.course_thumbnail.url}
      return representation
   
   
class BuyEbookSerializer(serializers.ModelSerializer):
   purchased_at = serializers.DateTimeField(format="%H:%M%p %Y-%m-%d", read_only=True)
   
   class Meta:
      model = MyEbooks
      fields = ['user', 'ebook', 'purchased_at']
      
   def to_representation(self, instance):
      representation = super(BuyEbookSerializer, self).to_representation(instance)
      representation['user'] = {
         "id": instance.user.id,
         "full_name": instance.user.full_name
      }
      representation['ebook'] = {
         "id": instance.ebook.id,
         "name": instance.ebook.name,
         "image": instance.ebook.image.url
      }
      return representation
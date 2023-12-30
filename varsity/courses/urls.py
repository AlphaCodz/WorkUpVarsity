from django.urls import path
from .views import MyCourse, TopicsByCourseView


urlpatterns = [
   path("my-courses", MyCourse.as_view(), name='my-courses'),
   path("topic/<int:course_id>", TopicsByCourseView.as_view(), name='my-topics')
]


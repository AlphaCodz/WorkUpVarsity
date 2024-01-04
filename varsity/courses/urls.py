from django.urls import path
from .views import MyCourse, TopicsByCourseView, CourseTopicsAndContentsAPIView
from courses.extras.views import MyCourses


urlpatterns = [
   path("my-courses", MyCourse.as_view(), name='my-courses'),
   path("topic/<int:course_id>", TopicsByCourseView.as_view(), name='my-topics'),
   path('courses/<int:pk>/topics-contents/', CourseTopicsAndContentsAPIView.as_view(), name='course-topics-contents'),
   path('paid-courses/<str:user>', MyCourses.as_view(), name='paid')
]
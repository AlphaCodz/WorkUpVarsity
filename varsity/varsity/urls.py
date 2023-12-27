from django.contrib import admin
from django.urls import path, include  # Import include
from rest_framework import routers
from main_app.views import SignUpStudent, SignUpInstructor
from courses.views import CreateCourse, CreateCourseContent, CreateCourseTopic, ReviewCourse, CourseOwnerShipView, CreateCourseCategory, CourseQuestion, CourseQuestionReply
from main_app.shop.views import CreateProductView

router = routers.DefaultRouter() 
router.register("signup", SignUpStudent, basename="signup-student")
router.register("reg/instructor", SignUpInstructor, basename="signup-instructor")
router.register("create/course", CreateCourse, basename="create-course")
router.register("create/content", CreateCourseContent, basename="content")
router.register("create/topic", CreateCourseTopic, basename="topic")
router.register("review", ReviewCourse, basename="review")
router.register("create/category", CreateCourseCategory, basename="create-category")
router.register("add/course", CourseOwnerShipView, basename="course-ownership")
router.register("ask/question", CourseQuestion, basename='question')
router.register("reply", CourseQuestionReply, basename="reply")
router.register("create/product", CreateProductView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('workup/', include(router.urls)),  # Use include to include the router's URLs
    path('varsity/', include('main_app.urls')),
    path('api/v1/', include('courses.urls'))
]
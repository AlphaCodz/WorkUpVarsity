from django.contrib import admin
from django.urls import path, include  # Import include
from rest_framework import routers
from main_app.views import SignUpStudent, SignUpInstructor, CreateHoldingAccount, MyReferredUsersView
from courses.views import CreateCourse, CreateCourseContent, CreateCourseTopic, ReviewCourse, CreateCourseCategory, CourseQuestion, CourseQuestionReply, StateView, AdminViewCourses
from main_app.shop.views import CreateProductView
from courses.ebooks.views import CreateEbook, BuyEbookView
from courses.extras.views import BuyCourseView, MakeOrder, BuyEbookView

router = routers.DefaultRouter() 
router.register("signup", SignUpStudent, basename="signup-student")
router.register("reg/instructor", SignUpInstructor, basename="signup-instructor")
router.register("create/course", CreateCourse, basename="create-course")
router.register("admin/courses", AdminViewCourses, basename="admincourses")
router.register("create/content", CreateCourseContent, basename="content")
router.register("create/topic", CreateCourseTopic, basename="topic")
router.register("review", ReviewCourse, basename="review")
router.register("create/category", CreateCourseCategory, basename="create-category")
# router.register("add/course", CourseOwnerShipView, basename="course-ownership")
router.register("ask/question", CourseQuestion, basename='question')
router.register("reply", CourseQuestionReply, basename="reply")
router.register("create/product", CreateProductView)
router.register("create/ebook", CreateEbook, basename='ebook')
router.register("buy/ebook", BuyEbookView, basename='bought-ebook')

router.register("buy/course", BuyCourseView, basename='bought-courses')
router.register("make-order", MakeOrder, basename='makeorders')

router.register("bank/account", CreateHoldingAccount, basename='holding-account')

router.register("process/state", StateView, basename='state')

router.register("referees", MyReferredUsersView, basename='referee')

# router.register('ebooks', BuyEbookView, basename='ebooks')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workup/', include(router.urls)),  # Use include to include the router's URLs
    path('varsity/', include('main_app.urls')),
    path('api/v1/', include('courses.urls'))
]
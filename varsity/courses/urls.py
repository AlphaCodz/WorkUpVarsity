from django.urls import path
from .views import MyCourse, TopicsByCourseView, CourseTopicsAndContentsAPIView
from courses.extras.views import MyCourses, ReplyByCourseView, AdminDashboardCounts
from courses.extras.payments import MakePayment, VerifyPayment, MakeTransfer, InitiateTransfer


urlpatterns = [
   path("my-courses", MyCourse.as_view(), name='my-courses'),
   path("topic/<int:course_id>", TopicsByCourseView.as_view(), name='my-topics'),
   path('courses/<int:pk>/topics-contents/', CourseTopicsAndContentsAPIView.as_view(), name='course-topics-contents'),
   path('paid-courses/<str:user>', MyCourses.as_view(), name='paid'),
   path('replies/<int:course_id>/', ReplyByCourseView.as_view(), name='reply_by_course'),
   path('dashboard/count', AdminDashboardCounts.as_view(), name='count'),
   path('make/payment', MakePayment.as_view(), name='payment'),
   path('verify/payment', VerifyPayment.as_view(), name='verify'),
   path('initiate/transfer', InitiateTransfer.as_view(), name='initiate-tranfer'),
   path('make/transfer', MakeTransfer.as_view(), name='make-transfer')
]
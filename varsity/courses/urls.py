from django.urls import path
from .views import MyCourse


urlpatterns = [
   path("my-courses", MyCourse.as_view(), name='my-courses')
]


"""
URL configuration for varsity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Import include
from rest_framework import routers
from main_app.views import SignUpStudent, SignUpInstructor
from courses.views import CreateCourse, CreateCourseContent, CreateCourseTopic

router = routers.DefaultRouter() 
router.register("signup", SignUpStudent, basename="signup-student")
router.register("reg/instructor", SignUpInstructor, basename="signup-instructor")
router.register("create/course", CreateCourse, basename="create-course")
router.register("create/content", CreateCourseContent, basename="content")
router.register("create/topic", CreateCourseTopic, basename="topic")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('workup/', include(router.urls)),  # Use include to include the router's URLs
    path('varsity/', include('main_app.urls')),
    # path('api/v1/', include('courses.urls'))
]
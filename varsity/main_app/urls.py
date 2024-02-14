from django.urls import path
from rest_framework_simplejwt.views import (
   TokenObtainSlidingView,
   TokenRefreshSlidingView,
)
from .views import SignInUserView, UpdatePassword

urlpatterns = [
   path('api/token/', SignInUserView.as_view(), name='token_obtain'),
   # path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
   path('update/password/', UpdatePassword.as_view(), name='update-pass')
]
from rest_framework import permissions
from main_app.models import MainUser

class SuperPermission(permissions.BasePermission):
   message = "You don't have permissions to carry out this request"

   def has_permission(self, request, view):
      # Check if the user is authenticated
      if request.user.is_authenticated:
         # Get the current user
         user = request.user
         
         # Check if user is_instructor is True
         if hasattr(user, 'is_instructor') and user.is_instructor:
               return True  # User is authenticated and has instructor permissions
      return False
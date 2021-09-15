from functools import wraps
from django.shortcuts import redirect



def user_is_logged_in(function):
     """
     This function checks whether the user is logged in if yes it will redirect to where the user should be.
     If the user go the login page or clicks the browser back button after log in it will
     redirect the user to dashboard.
     """
     @wraps(function)
     def wrap(request, *args, **kwargs):
     
          if request.user.is_authenticated:
               return redirect('dashboard:user_dashboard')
          else:
               return function(request, *args, **kwargs)
     return wrap
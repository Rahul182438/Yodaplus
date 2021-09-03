from functools import wraps
from django.shortcuts import redirect



def user_is_logged_in(function):
     @wraps(function)
     def wrap(request, *args, **kwargs):
     
          if request.user.is_authenticated:
               return redirect('dashboard:user_dashboard')
          else:
               return function(request, *args, **kwargs)
     return wrap
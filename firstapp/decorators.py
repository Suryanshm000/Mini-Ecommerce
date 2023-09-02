from functools import wraps
from django.shortcuts import redirect

def vendor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_vendor:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('firstapp:profile')  # Redirect to customer profile or login page
    return _wrapped_view

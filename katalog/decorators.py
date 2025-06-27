# decorators.py
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role == role:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied  # Atau redirect ke halaman lain
            else:
                return redirect('login')  # Ganti dengan nama URL login Anda
        return _wrapped_view
    return decorator
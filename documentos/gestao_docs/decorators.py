from django.shortcuts import redirect
from .models import GestorLocal

def check_permission(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        is_gestor = GestorLocal.objects.filter(user=user).exists()
        if is_gestor:
            return view_func(request, *args, **kwargs)
        
        return redirect('no_permission')
    return _wrapped_view

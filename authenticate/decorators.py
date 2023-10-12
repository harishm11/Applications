# from functools import wraps
# from django.http import HttpResponse, HttpResponseForbidden
# from django.contrib.auth.decorators import user_passes_test

# from .models import UserRole, Permission


# def has_permission(permission_name):
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             # Check if the user has the specified permission
#             if request.user.has_perm(permission_name):
#                 if request.user.userprofile.user_roles.name == 'dm':
#                     return view_func(request, *args, **kwargs)
#                 else:
#                     # Handle permission denied (e.g., return a 403 Forbidden response)
#                     return HttpResponseForbidden("Permission denied")
#             else:
#                 # Handle permission denied (e.g., return a 403 Forbidden response)
#                 return HttpResponseForbidden("Permission denied")

#         return _wrapped_view

#     return decorator


from django.http import HttpResponseForbidden


def permission_required(action):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Extract the app_label and model_name from the request or other sources.
            app_label = kwargs.get('appLabel')  # Adjust as needed.
            model_name = kwargs.get('modelName')  # Adjust as needed.
            permission_name = f'{app_label}.can_{action}_{model_name.lower()}'
            if request.user.has_perm(permission_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Permission denied")
        return _wrapped_view
    return decorator

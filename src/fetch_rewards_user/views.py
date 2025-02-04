from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

# Authentication and Authorization Decorators
def authenticate_session_token(view_func):
    def wrapper(request, *args, **kwargs):
        session_token = request.headers.get('X-Session-Token')
        if not session_token:
            logger.warning('Session token missing')
            return JsonResponse({'error': 'Session token missing'}, status=401)
        try:
            session = Session.objects.get(session_key=session_token)
            user_id = session.get_decoded().get('_auth_user_id')    
            user = User.objects.get(pk=user_id)
        except (Session.DoesNotExist, User.DoesNotExist):
            logger.warning('Invalid session token: %s', session_token)
            return JsonResponse({'error': 'Invalid session token'}, status=401)

        request.user = user
        request.user_id = user_id
        logger.info('User authenticated: %s', user.username)
        return view_func(request, *args, **kwargs)
    return wrapper

def permission_required(permission_code):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.has_perm(permission_code) or request.user.groups.filter(permissions__codename=permission_code).exists():
                    return view_func(request, *args, **kwargs)
            logger.warning('Access denied for user: %s, permission: %s', request.user.username, permission_code)
            return JsonResponse({'error': 'Access denied'}, status=403)  # Changed status code to 403
        return wrapper
    return decorator

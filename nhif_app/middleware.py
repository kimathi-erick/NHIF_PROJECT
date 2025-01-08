# myapp/middleware.py
import time
from django.conf import settings
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = int(time.time())
            last_activity = request.session.get('last_activity', current_time)
            
            # Check if the session has timed out
            if current_time - last_activity > settings.SESSION_COOKIE_AGE:
                logout(request)  # Log out the user
            else:
                request.session['last_activity'] = current_time  # Update last activity
                
        response = self.get_response(request)
        return response

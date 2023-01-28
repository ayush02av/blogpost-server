import jwt
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from database.models import User

def get_user(userinfo):
    user = User.objects.get(
        username = userinfo['username']
    )
    return user

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'path') and not 'auth' in request.path:
            if 'token' not in request.COOKIES:
                response = Response({
                    'message':'Not logged in'
                }, status=status.HTTP_401_UNAUTHORIZED)

                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()

                return response
            
            token = request.COOKIES['token']
            decoded = jwt.decode(token, options={"verify_signature": False})
            request.user = get_user(decoded)

        response = self.get_response(request)
        return response
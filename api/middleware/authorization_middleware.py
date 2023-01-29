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
    public_allowed_urls = [
        'auth',
        'public'
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'path') and 'api' in request.path:
            if request.path.split('/')[2] not in self.public_allowed_urls:
                if 'Authorization' not in request.headers.keys():
                    response = Response({
                        'message':'Not logged in'
                    }, status=status.HTTP_401_UNAUTHORIZED)

                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()

                    return response
            
                token = request.headers['Authorization']
                decoded = jwt.decode(token, options={"verify_signature": False})
                request.user = get_user(decoded)

        response = self.get_response(request)
        return response
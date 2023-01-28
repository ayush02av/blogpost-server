from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from api.serializers import serializers_user
import jwt
from django.conf import settings

def get_authenticated_user_and_token(instance):
    user = serializers_user.user_serializer(serializers_user.models.User.objects.get(username = instance['username']), many=False)
    user = user.data

    token = jwt.encode({
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }, settings.JWT_SECRET, algorithm="HS256")

    return {
        'user': user,
        'token': token
    }
    
class signup_user(generics.CreateAPIView):
    queryset = serializers_user.models.User.objects.all()
    serializer_class = serializers_user.signup_user_serializer
    
    def post(self, request):
        instance = self.create(request)
        
        return Response({
                'message': 'New user created',
                'user': get_authenticated_user_and_token(instance.data)
            }, status=status.HTTP_201_CREATED)